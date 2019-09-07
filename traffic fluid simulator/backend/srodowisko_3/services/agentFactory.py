from typing import List

from tensorflow.python.keras.models import load_model

from model.SmartAgent import SmartAgent


def get_LearnSmartAgents(file_names=None) -> List[SmartAgent]:
    models = []
    if file_names == None:
        file_names = ['static_files/model-agent0.h5', 'static_files/model-agent1.h5', 'static_files/model-agent2.h5']
    for i in range(len(file_names)):
        model = load_model(file_names[i])
        models.append(model)
    return get_SmartAgents_with_model(models)


def get_SmartAgents() -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[((9, 2), (21, 2), (27, 17)),
                                ((21, 20), (27, 20), (9, 2)),
                                ((27, 17), (9, 17), (21, 20))],
                         local_phase_sections=[2, 20, 17],
                         curve_densities={(9, 2): 0.7, (21, 2): 0.3,
                                          (21, 20): 0.3, (27, 20): 0.7,
                                          (27, 17): 0.7, (9, 17): 0.3},
                         outflow_section=27)
    agent_1 = SmartAgent(index=1,
                         moves=[((12, 11), (30, 11), (18, 26)),
                                ((12, 5), (18, 5), (30, 11)),
                                ((18, 26), (30, 26), (12, 5))],
                         local_phase_sections=[5, 26, 11],
                         curve_densities={(12, 5): 0.7, (18, 5): 0.3,
                                          (30, 11): 0.7, (12, 11): 0.3,
                                          (18, 26): 0.3, (30, 26): 0.7},
                         outflow_section=30)
    agent_2 = SmartAgent(index=2,
                         moves=[((33, 14), (15, 14), (24, 23)),
                                ((24, 8), (15, 8), (33, 14)),
                                ((24, 23), (33, 23), (15, 8))],
                         local_phase_sections=[8, 14, 23],
                         curve_densities={(15, 8): 0.7, (24, 8): 0.3,
                                          (33, 14): 0.7, (15, 14): 0.3,
                                          (24, 23): 0.3, (33, 23): 0.7},
                         outflow_section=33)
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
                         model=models[0],
                         outflow_section=27)
    agent_1 = SmartAgent(index=1,
                         moves=[((12, 11), (30, 11), (18, 26)),
                                ((12, 5), (18, 5), (30, 11)),
                                ((18, 26), (30, 26), (12, 5))],
                         local_phase_sections=[5, 26, 11],
                         curve_densities={(12, 5): 0.7, (18, 5): 0.3,
                                          (30, 11): 0.7, (12, 11): 0.3,
                                          (18, 26): 0.7, (30, 26): 0.3},
                         model=models[1],
                         outflow_section=30)  # blad
    agent_2 = SmartAgent(index=2,
                         moves=[((33, 14), (15, 14), (24, 23)),
                                ((24, 8), (15, 8), (33, 14)),
                                ((24, 23), (33, 23), (15, 8))],
                         local_phase_sections=[8, 14, 23],
                         curve_densities={(15, 8): 0.7, (24, 8): 0.3,
                                          (33, 14): 0.7, (15, 14): 0.3,
                                          (24, 23): 0.7, (33, 23): 0.3},
                         model=models[2],
                         outflow_section=33)
    agents.append(agent_0)
    agents.append(agent_1)
    agents.append(agent_2)
    return agents