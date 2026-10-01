from enum import StrEnum

from sqlalchemy import Enum


class Role(StrEnum):
    OPERATOR = "operator"
    ENGINEER = "engineer"
    ADMIN = "admin"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(StrEnum):
    OPEN = "open"
    IN_ANALYSIS = "in_analysis"
    CORRECTIVE_ACTION = "corrective_action"
    CLOSED = "closed"


def enum_column_type(enum_class: type[StrEnum], name: str | None = None) -> Enum:
    """Guarda el enum como texto (VARCHAR) con un CHECK que solo admite sus valores.

    `name` da nombre al CHECK; hace falta si una tabla usa el mismo enum en dos columnas.
    """
    return Enum(
        enum_class,
        name=name or enum_class.__name__.lower(),
        native_enum=False,
        create_constraint=True,
        length=30,
        values_callable=lambda members: [member.value for member in members],
    )
