from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.models import Incident, Part, User
from app.models.enums import IncidentStatus, Severity
from app.schemas.incident_schema import IncidentCreate, IncidentUpdate
from app.services import part_service
from app.services.incident_history_service import record_event

# Flujo permitido: open → in_analysis → corrective_action → closed
ALLOWED_TRANSITIONS = {
    IncidentStatus.OPEN: IncidentStatus.IN_ANALYSIS,
    IncidentStatus.IN_ANALYSIS: IncidentStatus.CORRECTIVE_ACTION,
    IncidentStatus.CORRECTIVE_ACTION: IncidentStatus.CLOSED,
}


def list_incidents(
    db: Session,
    status: IncidentStatus | None = None,
    severity: Severity | None = None,
    supplier_id: int | None = None,
) -> list[Incident]:
    query = select(Incident).order_by(Incident.created_at.desc())
    if status is not None:
        query = query.where(Incident.status == status)
    if severity is not None:
        query = query.where(Incident.severity == severity)
    if supplier_id is not None:
        query = query.join(Incident.part).where(Part.supplier_id == supplier_id)
    return list(db.scalars(query))


def get_incident(db: Session, incident_id: int) -> Incident:
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise NotFoundError("Incident", incident_id)
    return incident


def create_incident(db: Session, data: IncidentCreate, current_user: User) -> Incident:
    part_service.get_part(db, data.part_id)
    incident = Incident(**data.model_dump(), reported_by_id=current_user.id)
    db.add(incident)
    record_event(db, incident, current_user, "created", to_status=IncidentStatus.OPEN)
    db.commit()
    db.refresh(incident)
    return incident


def update_incident(
    db: Session, incident_id: int, data: IncidentUpdate, current_user: User
) -> Incident:
    incident = get_incident(db, incident_id)
    ensure_not_closed(incident)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    record_event(db, incident, current_user, "updated")
    db.commit()
    db.refresh(incident)
    return incident


def change_status(
    db: Session, incident_id: int, new_status: IncidentStatus, current_user: User
) -> Incident:
    incident = get_incident(db, incident_id)
    _ensure_transition_allowed(incident, new_status)
    if new_status == IncidentStatus.CORRECTIVE_ACTION and incident.action_plan is None:
        raise BusinessRuleError("Create an action plan to move to corrective action")
    if new_status == IncidentStatus.CLOSED:
        _ensure_plan_is_completed(incident)
    apply_status_change(db, incident, new_status, current_user, "status_changed")
    db.commit()
    db.refresh(incident)
    return incident


def apply_status_change(
    db: Session, incident: Incident, new_status: IncidentStatus, current_user: User, action: str
) -> None:
    """Cambia el estado y lo anota en el historial, sin hacer commit."""
    _ensure_transition_allowed(incident, new_status)
    old_status = incident.status
    incident.status = new_status
    if new_status == IncidentStatus.IN_ANALYSIS:
        incident.analyzed_by_id = current_user.id
    if new_status == IncidentStatus.CLOSED:
        incident.closed_at = datetime.now(UTC)
    record_event(db, incident, current_user, action, old_status, new_status)


def ensure_not_closed(incident: Incident) -> None:
    if incident.status == IncidentStatus.CLOSED:
        raise BusinessRuleError(f"Incident {incident.id} is closed")


def _ensure_transition_allowed(incident: Incident, new_status: IncidentStatus) -> None:
    if ALLOWED_TRANSITIONS.get(incident.status) != new_status:
        raise BusinessRuleError(f"Cannot change status from '{incident.status}' to '{new_status}'")


def _ensure_plan_is_completed(incident: Incident) -> None:
    plan = incident.action_plan
    if plan is None or not plan.tasks:
        raise BusinessRuleError("The action plan needs at least one task before closing")
    if any(task.completed_at is None for task in plan.tasks):
        raise BusinessRuleError("All action plan tasks must be completed before closing")
