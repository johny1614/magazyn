import random
from typing import List

from tensorflow.python.keras.models import load_model

from model.LearningState import LearningState
from model.SmartAgent import SmartAgent


def get_LearnSmartAgents() -> List[SmartAgent]:
    agents = get_SmartAgents()
    for agent in agents:
        file_name = 'agent' + str(agent.index) + '.h5'
        model = load_model(file_name)
        agent.model = model
    return agents


def get_SmartAgents() -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[(),
                                ((9, 2), (21, 2), (27, 17)),
                                ((21, 20), (27, 20), (9, 2)),
                                ((27, 17), (9, 17), (21, 20))],
                         local_phase_sections=[2, 20, 17],
                         curve_densities={(9, 2): 0.7, (21, 2): 0.3,
                                          (21, 20): 0.7, (27, 20): 0.3,
                                          (27, 17): 0.7, (9, 17): 0.3},
                         sections_9_indexes=[0, 1, 2, 18, 19, 20, 15, 16, 17])
    agent_1 = SmartAgent(index=1,
                         moves=[(),
                                ((12, 11), (30, 11), (18, 26)),
                                ((12, 5), (18, 5), (30, 11)),
                                ((18, 26), (30, 26), (12, 5))],
                         local_phase_sections=[5, 11, 26],
                         curve_densities={(12, 5): 0.7, (18, 5): 0.3,
                                          (30, 11): 0.7, (12, 11): 0.3,
                                          (18, 26): 0.7, (30, 26): 0.3},
                         sections_9_indexes=[3, 4, 5, 24, 25, 26, 9, 10, 11])
    agent_2 = SmartAgent(index=2,
                         moves=[(),
                                ((33, 14), (15, 14), (24, 23)),
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
