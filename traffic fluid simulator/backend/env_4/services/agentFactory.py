from model.Agent import Agent
from model.SmartAgent import SmartAgent


def get_Agents():
    agent_1_dic = {'all_phases': [[[]], [(9, 2), (21, 2), (27, 17)],
                                  [(21, 20), (27, 20), (9, 2)],
                                  [(27, 17), (9, 17), (21, 20)]],
                   'actual_phase': [[]],
                   'actual_phase_duration': 0,
                   'curve_densities': {(9, 2): 0.7, (21, 2): 0.3,
                                       (21, 20): 0.7, (27, 20): 0.3,
                                       (27, 17): 0.7, (9, 17): 0.3},
                   'local_phase_sections': [2, 20, 17]}
    agent_2_dic = {'all_phases': [[[]], [(12, 11), (30, 11), (18, 26)],
                                  [(12, 5), (18, 5), (30, 11)],
                                  [(18, 26), (30, 26), (12, 5)]],
                   'actual_phase': [(12, 11), (30, 11), (18, 26)],
                   'actual_phase_duration': 0,
                   'curve_densities': {(12, 5): 0.7, (18, 5): 0.3,
                                       (30, 11): 0.7, (12, 11): 0.3,
                                       (18, 26): 0.7, (30, 26): 0.3},
                   'local_phase_sections': [5, 11, 26]
                   }
    agent_3_dic = {'all_phases': [[[]], [(33, 14), (15, 14), (24, 23)],
                                  [(24, 8), (15, 8), (33, 14)],
                                  [(24, 23), (33, 23), (15, 8)]
                                  ],
                   'actual_phase': [(33, 14), (15, 14), (24, 23)],
                   'actual_phase_duration': 0,
                   'curve_densities': {(15, 8): 0.7, (24, 8): 0.3,
                                       (33, 14): 0.7, (15, 14): 0.3,
                                       (24, 23): 0.7, (33, 23): 0.3},
                   'local_phase_sections': [8, 14, 23]
                   }
    agents = [Agent(dic=agent_1_dic, min_phase_duration=3, index=1, orange_phase_duration=1),
              Agent(dic=agent_2_dic, min_phase_duration=3, index=2, orange_phase_duration=1),
              Agent(dic=agent_3_dic, min_phase_duration=3, index=3, orange_phase_duration=1)]
    return agents

def get_SmartAgents():
    agent_1_dic = {'all_phases': [[[]], [(9, 2), (21, 2), (27, 17)],
                                  [(21, 20), (27, 20), (9, 2)],
                                  [(27, 17), (9, 17), (21, 20)]],
                   'actual_phase': [[]],
                   'actual_phase_duration': 0,
                   'curve_densities': {(9, 2): 0.7, (21, 2): 0.3,
                                       (21, 20): 0.7, (27, 20): 0.3,
                                       (27, 17): 0.7, (9, 17): 0.3},
                   'local_phase_sections': [2, 20, 17]}
    agent_2_dic = {'all_phases': [[[]], [(12, 11), (30, 11), (18, 26)],
                                  [(12, 5), (18, 5), (30, 11)],
                                  [(18, 26), (30, 26), (12, 5)]],
                   'actual_phase': [(12, 11), (30, 11), (18, 26)],
                   'actual_phase_duration': 0,
                   'curve_densities': {(12, 5): 0.7, (18, 5): 0.3,
                                       (30, 11): 0.7, (12, 11): 0.3,
                                       (18, 26): 0.7, (30, 26): 0.3},
                   'local_phase_sections': [5, 11, 26]
                   }
    agent_3_dic = {'all_phases': [[[]], [(33, 14), (15, 14), (24, 23)],
                                  [(24, 8), (15, 8), (33, 14)],
                                  [(24, 23), (33, 23), (15, 8)]
                                  ],
                   'actual_phase': [(33, 14), (15, 14), (24, 23)],
                   'actual_phase_duration': 0,
                   'curve_densities': {(15, 8): 0.7, (24, 8): 0.3,
                                       (33, 14): 0.7, (15, 14): 0.3,
                                       (24, 23): 0.7, (33, 23): 0.3},
                   'local_phase_sections': [8, 14, 23]
                   }
    agents = [SmartAgent(dic=agent_1_dic, min_phase_duration=3, index=1, orange_phase_duration=1),
              SmartAgent(dic=agent_2_dic, min_phase_duration=3, index=2, orange_phase_duration=1),
              SmartAgent(dic=agent_3_dic, min_phase_duration=3, index=3, orange_phase_duration=1)]
    return agents
