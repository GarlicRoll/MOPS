
from dataclasses import dataclass
from typing import Optional

import operator

OPS = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}


@dataclass
class Rule:
    id: str
    type: str # instant | duration
    field: str
    operator: str
    value: float
    severity: str
    message: str

    # для duration
    count: Optional[int] = None # сколько подряд событий
    entity_field: Optional[str] = None # device_id (в теории можно другое)

