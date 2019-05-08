from model.LearningState import LearningState

state_1 = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 5), phase_no=2, phase_duration=1)
different_state = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 8), phase_no=2, phase_duration=1)
state_1_also = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 5), phase_no=2, phase_duration=1)
myDic = {state_1: [2], different_state: [6]}
myDic[state_1_also].append(6)
print(myDic[state_1])
