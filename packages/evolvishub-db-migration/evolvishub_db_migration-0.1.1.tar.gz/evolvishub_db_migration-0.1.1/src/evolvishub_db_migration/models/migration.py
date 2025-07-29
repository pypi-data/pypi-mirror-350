from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Migration:
    name: str
    version: str
    sql: str
    applied_at: Optional[datetime] = None
