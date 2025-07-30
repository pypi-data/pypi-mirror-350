import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
from typing import Callable, Optional

from easybits_module_interface.models import Message


@dataclass
class GenerationRequest:
    """
    Dataclass to hold the request for a generation task.
    """
    message: Message
    method: Callable
    verbose: int
    timeout: int
    owner_id: str = field(default_factory=lambda: 'unknown')
    timestamp: datetime = field(default_factory=datetime.now)
    notified: bool = False
    task_id: int = field(default_factory=count().__next__, init=False)
    # timeout in minutes
    execution_timestamp: Optional[datetime] = None
    execution_timeout: int | float = 30

    def __post_init__(self):
        if self.verbose == 0:
            self.notified = True


@dataclass
class RunningTask:
    """
    Dataclass to hold the running tasks.
    """
    generation_request: GenerationRequest
    task: asyncio.Future

