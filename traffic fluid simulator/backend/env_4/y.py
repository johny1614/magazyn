from model.LearningState import LearningState

ls = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 5), phase_no=2, phase_duration=1)
ls2 = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 8), phase_no=2, phase_duration=1)
ls3 = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 5), phase_no=2, phase_duration=1)
myDic = {ls: [2], ls2: [345]}
myDic[ls3].append(235)
print(myDic[ls])
