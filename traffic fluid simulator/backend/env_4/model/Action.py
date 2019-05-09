from dataclasses import dataclass

from model import Phase
from services.hashable_decorator import hashable


@hashable
@dataclass
class Action:
    index: int
    agent_index: int
    decided_phase: Phase
