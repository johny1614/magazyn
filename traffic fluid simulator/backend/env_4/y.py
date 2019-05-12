import attr
from model.LearningState import LearningState


@attr.s(auto_attribs=True)
class AgentWithState:
    state: LearningState = None


state = LearningState(pre_cross_densities=(2, 3),
                      global_aggregated_densities=(1, 17),
                      phase_index=2,
                      phase_duration=24)
state_2 = LearningState(pre_cross_densities=(7, 8),
                        global_aggregated_densities=(4, 22),
                        phase_index=6,
                        phase_duration=14)
state_3 = LearningState(pre_cross_densities=(32, 12),
                        global_aggregated_densities=(21, 22),
                        phase_index=22,
                        phase_duration=2)
agent_1 = AgentWithState(state)
agent_2 = AgentWithState(state_2)
print(state)
print(state_2)
print(agent_1)
print(agent_2)
agent_1.state=state_3
print(agent_1)
print(agent_2)


