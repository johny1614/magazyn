import random
from typing import List

from tensorflow.python.keras.models import load_model

from model.LearningState import LearningState
from model.SmartAgent import SmartAgent


def get_LearnSmartAgents(file_names=None) -> List[SmartAgent]:
    models = []
    if file_names == None:
        file_names = ['static_files/model-agent0.h5', 'static_files/model-agent1.h5', 'static_files/model-agent2.h5']
    for i in range(3):
        model = load_model(file_names[i])
        models.append(model)
    return get_SmartAgents_with_model(models)


def deep_copy_agent(agent):
    new_agent = SmartAgent(index=agent.index,
                           moves=agent.moves,
                           local_phase_sections=agent.local_phase_sections,
                           curve_densities=agent.curve_densities,
                           sections_9_indexes=agent.sections_9_indexes)
    new_agent.local_state = agent.local_state
    new_agent.orange_phase_duration = agent.orange_phase_duration
    new_agent.pending_phase = agent.pending_phase
    new_agent.rewards = agent.rewards
    new_agent.actual_phase = agent.actual_phase
    new_agent.starting_actual_phase = agent.starting_actual_phase
    new_agent.action = agent.action
    return new_agent

def get_SmartAgents() -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[((9, 2), (21, 2), (27, 17)),
                                ((21, 20), (27, 20), (9, 2)),
                                ((27, 17), (9, 17), (21, 20))],
                         local_phase_sections=[2, 20, 17],
                         curve_densities={(9, 2): 0.7, (21, 2): 0.3,
                                          (21, 20): 0.7, (27, 20): 0.3,
                                          (27, 17): 0.7, (9, 17): 0.3},
                         sections_9_indexes=[0, 1, 2, 18, 19, 20, 15, 16, 17])
    agent_1 = SmartAgent(index=1,
                         moves=[((12, 11), (30, 11), (18, 26)),
                                ((12, 5), (18, 5), (30, 11)),
                                ((18, 26), (30, 26), (12, 5))],
                         local_phase_sections=[5, 11, 26],
                         curve_densities={(12, 5): 0.7, (18, 5): 0.3,
                                          (30, 11): 0.7, (12, 11): 0.3,
                                          (18, 26): 0.7, (30, 26): 0.3},
                         sections_9_indexes=[3, 4, 5, 24, 25, 26, 9, 10, 11])
    agent_2 = SmartAgent(index=2,
                         moves=[((33, 14), (15, 14), (24, 23)),
                                ((24, 8), (15, 8), (33, 14)),
                                ((24, 23), (33, 23), (15, 8))],
                         local_phase_sections=[8, 14, 23],
                         curve_densities={(15, 8): 0.7, (24, 8): 0.3,
                                          (33, 14): 0.7, (15, 14): 0.3,
                                          (24, 23): 0.7, (33, 23): 0.3},
                         sections_9_indexes=[6, 7, 8, 21, 22, 23, 12, 13, 14])
    agents.append(agent_0)
    agents.append(agent_1)
    agents.append(agent_2)
    return agents

def get_SmartAgents_with_model(models) -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[((9, 2), (21, 2), (27, 17)),
                                ((21, 20), (27, 20), (9, 2)),
                                ((27, 17), (9, 17), (21, 20))],
                         local_phase_sections=[2, 20, 17],
                         curve_densities={(9, 2): 0.7, (21, 2): 0.3,
                                          (21, 20): 0.7, (27, 20): 0.3,
                                          (27, 17): 0.7, (9, 17): 0.3},
                         sections_9_indexes=[0, 1, 2, 18, 19, 20, 15, 16, 17],
                         model=models[0])
    agent_1 = SmartAgent(index=1,
                         moves=[((12, 11), (30, 11), (18, 26)),
                                ((12, 5), (18, 5), (30, 11)),
                                ((18, 26), (30, 26), (12, 5))],
                         local_phase_sections=[5, 11, 26],
                         curve_densities={(12, 5): 0.7, (18, 5): 0.3,
                                          (30, 11): 0.7, (12, 11): 0.3,
                                          (18, 26): 0.7, (30, 26): 0.3},
                         sections_9_indexes=[3, 4, 5, 24, 25, 26, 9, 10, 11],
                         model=models[1])
    agent_2 = SmartAgent(index=2,
                         moves=[((33, 14), (15, 14), (24, 23)),
                                ((24, 8), (15, 8), (33, 14)),
                                ((24, 23), (33, 23), (15, 8))],
                         local_phase_sections=[8, 14, 23],
                         curve_densities={(15, 8): 0.7, (24, 8): 0.3,
                                          (33, 14): 0.7, (15, 14): 0.3,
                                          (24, 23): 0.7, (33, 23): 0.3},
                         sections_9_indexes=[6, 7, 8, 21, 22, 23, 12, 13, 14],
                         model=models[2])
    agents.append(agent_0)
    agents.append(agent_1)
    agents.append(agent_2)
    return agents
# agents = get_SmartAgents()
# modelz=[agent.model for agent in agents]
# agents_with_model = get_SmartAgents_with_model(modelz)
#
# a=2
