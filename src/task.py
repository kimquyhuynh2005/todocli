from dataclasses import dataclass,field
from typing import List, Optional
from datetime import datetime, timedelta

@dataclass
class Task:
    id: int
    title: str
    status: str = field(default='todo')
    created_at: str = field(repr=False, 
                            default_factory=lambda: datetime.now().isoformat())
    due_to: Optional[str] = field(default=None)

    @property
    def remaining_time(self) -> Optional[timedelta]:
        if self.due_to:
            due_dt = datetime.strptime(self.due_to, '%Y-%m-%d')     
            return due_dt - datetime.now()
        return None
