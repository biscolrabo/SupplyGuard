from sqlalchemy.orm import Session

from app.models import Incident, IncidentHistory, User
from app.models.enums import IncidentStatus


def record_event(
    db: Session,
    incident: Incident,
    user: User,
    action: str,
    from_status: IncidentStatus | None = None,
    to_status: IncidentStatus | None = None,
) -> None:
    # No hace commit: el evento se guarda en la misma transacción que el cambio que registra
    db.add(
        IncidentHistory(
            incident=incident,
            user_id=user.id,
            action=action,
            from_status=from_status,
            to_status=to_status,
        )
    )
