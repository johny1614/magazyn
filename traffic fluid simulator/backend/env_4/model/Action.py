from model import Phase
import attr

@attr.s(auto_attribs=True,frozen=True)
class Action:
    index: int
    agent_index: int
    decided_phase: Phase
