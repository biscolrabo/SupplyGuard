from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.models import ActionPlan, Task, User
from app.models.enums import IncidentStatus
from app.schemas.action_plan_schema import ActionPlanCreate, ActionPlanUpdate
from app.services import incident_service, user_service
from app.services.incident_history_service import record_event


def get_action_plan(db: Session, plan_id: int) -> ActionPlan:
    plan = db.get(ActionPlan, plan_id)
    if plan is None:
        raise NotFoundError("Action plan", plan_id)
    return plan


def get_action_plan_by_incident(db: Session, incident_id: int) -> ActionPlan:
    incident_service.get_incident(db, incident_id)
    plan = db.scalar(select(ActionPlan).where(ActionPlan.incident_id == incident_id))
    if plan is None:
        raise NotFoundError("Action plan for incident", incident_id)
    return plan


def create_action_plan(
    db: Session, incident_id: int, data: ActionPlanCreate, current_user: User
) -> ActionPlan:
    incident = incident_service.get_incident(db, incident_id)
    if incident.action_plan is not None:
        raise ConflictError(f"Incident {incident_id} already has an action plan")
    if incident.status != IncidentStatus.IN_ANALYSIS:
        raise BusinessRuleError("An action plan can only be created for incidents in analysis")
    for task_data in data.tasks:
        user_service.get_active_user(db, task_data.assigned_to_id)

    plan = ActionPlan(
        incident=incident,
        created_by_id=current_user.id,
        description=data.description,
        tasks=[Task(**task_data.model_dump()) for task_data in data.tasks],
    )
    db.add(plan)
    # Crear el plan hace avanzar la incidencia a "acción correctiva"
    incident_service.apply_status_change(
        db, incident, IncidentStatus.CORRECTIVE_ACTION, current_user, "action_plan_created"
    )
    db.commit()
    db.refresh(plan)
    return plan


def update_action_plan(
    db: Session, plan_id: int, data: ActionPlanUpdate, current_user: User
) -> ActionPlan:
    plan = get_action_plan(db, plan_id)
    incident_service.ensure_not_closed(plan.incident)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(plan, field, value)
    record_event(db, plan.incident, current_user, "action_plan_updated")
    db.commit()
    db.refresh(plan)
    return plan
