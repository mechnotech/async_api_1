import datetime
from typing import Optional

from .common import AdvancedJsonModel


class PersonShort(AdvancedJsonModel):
    id: str
    full_name: str
    birthday: Optional[datetime.date]


class Person(PersonShort):
    role: Optional[dict]
