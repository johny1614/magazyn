from typing import List

from tensorflow.python.keras.models import load_model

from model.SmartAgent import SmartAgent


def get_LearnSmartAgents(file_names=None) -> List[SmartAgent]:
    models = []
    if file_names == None:
        file_names = ['static_files/model-agent0.h5', 'static_files/model-agent1.h5', 'static_files/model-agent2.h5','static_files/model-agent3.h5']
    for i in range(len(file_names)):
        model = load_model(file_names[i])
        models.append(model)
    return get_SmartAgents_with_model(models)


# w prawo 0.3 w lewo 0.2 prosto 0.5
def get_SmartAgents() -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[((1, 0), (2, 28)),
                                ((4, 37), (29, 21)),
                                ((4, 0), (2, 0), (29, 28), (1, 28)),
                                ((2, 37), (29, 37), (1, 21), (4, 21))],
                         local_phase_sections=[0, 21, 28, 37],
                         curve_densities={(4, 0): 0.5, (2, 0): 0.3, (1, 0): 0.2,
                                          (2, 37): 0.5, (29, 37): 0.3, (4, 37): 0.2,
                                          (2, 37): 0.5, (29, 37): 0.3, (4, 37): 0.2,
                                          (29, 28): 0.5, (1, 28): 0.3, (2, 28): 0.2,
                                          (1, 21): 0.5, (4, 21): 0.3, (29, 21): 0.2, },
                         outflow_section=27)
    agent_1 = SmartAgent(index=1,
                         moves=[((20, 30), (32, 17)),
                                ((20, 17), (19, 17),(33,30),(32,30)),
                                ((33, 18), (20,18), (19, 18)),
                                ((33, 3), (32, 3), (19, 3))],
                         local_phase_sections=[30, 18, 17, 3],
                         curve_densities={(33, 30): 0.5, (32, 30): 0.3, (20, 30): 0.2,
                                          (32, 3): 0.5, (19, 3): 0.3, (33, 3): 0.2,
                                          (20, 18): 0.5, (33, 18): 0.3, (19, 18): 0.2,
                                          (19, 17): 0.5, (20, 17): 0.3, (32, 17): 0.2, },
                         outflow_section=30)
    agent_2 = SmartAgent(index=2,
                         moves=[((8, 7), (10, 24)),
                                ((9, 31), (25, 23)),
                                ((9, 7), (10, 7), (8,24),(25,24)),
                                ((9, 23), (8, 23), (10, 31), (25, 31))],
                         local_phase_sections=[7, 23, 24, 31],
                         curve_densities={(9, 7): 0.5, (10, 7): 0.3, (8, 7): 0.2,
                                          (8, 23): 0.5, (9, 23): 0.3, (25, 23): 0.2,
                                          (25, 24): 0.5, (8, 24): 0.3, (10, 24): 0.2,
                                          (10, 31): 0.5, (25, 31): 0.3, (9, 31): 0.2, },
                         outflow_section=33)
    agent_3 = SmartAgent(index=3,
                         moves=[((22, 36), (13, 38)),
                                ((12, 11), (14, 39)),
                                ((13, 36), (12, 36), (14, 38), (22, 38)),
                                ((13, 11), (14, 11), (12, 39), (22, 39))],
                         local_phase_sections=[11, 36, 38, 39],
                         curve_densities={(12, 36): 0.5, (13, 36): 0.3, (22, 36): 0.2,
                                          (22, 39): 0.5, (12, 39): 0.3, (14, 39): 0.2,
                                          (14, 38): 0.5, (22, 38): 0.3, (13, 38): 0.2,
                                          (13, 11): 0.5, (14, 11): 0.3, (12, 11): 0.2, },
                         outflow_section=33)
    agents.append(agent_0)
    agents.append(agent_1)
    agents.append(agent_2)
    agents.append(agent_3)
    return agents


def get_SmartAgents_with_model(models) -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[((1, 0), (2, 28)),
                                ((4, 37), (29, 21)),
                                ((4, 0), (2, 0), (29, 28), (1, 28)),
                                ((2, 37), (29, 37), (1, 21), (4, 21))],
                         local_phase_sections=[0, 21, 28, 37],
                         curve_densities={(4, 0): 0.5, (2, 0): 0.3, (1, 0): 0.2,
                                          (2, 37): 0.5, (29, 37): 0.3, (4, 37): 0.2,
                                          (2, 37): 0.5, (29, 37): 0.3, (4, 37): 0.2,
                                          (29, 28): 0.5, (1, 28): 0.3, (2, 28): 0.2,
                                          (1, 21): 0.5, (4, 21): 0.3, (29, 21): 0.2, },
                         model=models[0],
                         outflow_section=27)
    agent_1 = SmartAgent(index=1,
                         moves=[((20, 30), (32, 17)),
                                ((33, 3), (19, 18)),
                                ((33, 30), (32, 30), (19, 17), (20, 17)),
                                ((32, 3), (19, 3), (33, 18), (20, 18))],
                         local_phase_sections=[30, 18, 17, 3],
                         curve_densities={(33, 30): 0.5, (32, 30): 0.3, (20, 30): 0.2,
                                          (32, 3): 0.5, (19, 3): 0.3, (33, 3): 0.2,
                                          (20, 18): 0.5, (33, 18): 0.3, (19, 18): 0.2,
                                          (19, 17): 0.5, (20, 17): 0.3, (32, 17): 0.2, },
                         model=models[1],
                         outflow_section=30)  # blad
    agent_2 = SmartAgent(index=2,
                         moves=[((8, 7), (10, 24)),
                                ((9, 31), (25, 23)),
                                ((9, 7), (10, 7), (8, 24), (25, 24)),
                                ((9, 23), (8, 23), (10, 31), (25, 31))],
                         local_phase_sections=[7, 23, 24, 31],
                         curve_densities={(9, 7): 0.5, (10, 7): 0.3, (8, 7): 0.2,
                                          (8, 23): 0.5, (9, 23): 0.3, (25, 23): 0.2,
                                          (25, 24): 0.5, (8, 24): 0.3, (10, 24): 0.2,
                                          (10, 31): 0.5, (25, 31): 0.3, (9, 31): 0.2, },
                         model=models[2],
                         outflow_section=33)
    agent_3 = SmartAgent(index=3,
                         moves=[((22, 36), (13, 38)),
                                ((12, 11), (14, 39)),
                                ((13, 36), (12, 36), (14, 38), (22, 38)),
                                ((13, 11), (14, 11), (12, 39), (22, 39))],
                         local_phase_sections=[11, 36, 38, 39],
                         curve_densities={(12, 36): 0.5, (13, 36): 0.3, (22, 36): 0.2,
                                          (22, 39): 0.5, (12, 39): 0.3, (14, 39): 0.2,
                                          (14, 38): 0.5, (22, 38): 0.3, (13, 38): 0.2,
                                          (13, 11): 0.5, (14, 11): 0.3, (12, 11): 0.2, },
                         model=models[3],
                         outflow_section=33)
    agents.append(agent_0)
    agents.append(agent_1)
    agents.append(agent_2)
    agents.append(agent_3)
    return agents
