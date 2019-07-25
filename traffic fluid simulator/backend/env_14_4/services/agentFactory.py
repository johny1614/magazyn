from typing import List

from tensorflow.python.keras.models import load_model

from model.SmartAgent import SmartAgent


def get_LearnSmartAgents(file_names=None) -> List[SmartAgent]:
    models = []
    if file_names == None:
        file_names = ['static_files/model-agent0.h5']
    for i in range(1):
        model = load_model(file_names[i])
        models.append(model)
    return get_SmartAgents_with_model(models)


def get_SmartAgents() -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[((4, 1), (404, 404)),
                                ((4, 3), (404, 404)),
                                ],
                         local_phase_sections=[0,1,2,3],
                         curve_densities={(4, 1): 1, (4, 3): 1})
    agents.append(agent_0)
    return agents


def get_SmartAgents_with_model(models) -> List[SmartAgent]:
    agents: SmartAgent = []
    agent_0 = SmartAgent(index=0,
                         moves=[((4, 1), (404, 404)),
                                ((4, 3), (404, 404)),
                                ],
                         local_phase_sections=[0,1,2,3],
                         curve_densities={(4, 1): 1, (4, 3): 1},
                         model = models[0])
    agents.append(agent_0)
    return agents
