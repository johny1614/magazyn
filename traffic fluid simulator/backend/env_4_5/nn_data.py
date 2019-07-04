from model.LearningState import LearningState
from services.parser import to_array

S1=[]
S1.append(LearningState(pre_cross_densities=(1, 0, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0), actual_phase=3, phase_duration=3))
S1.append(LearningState(pre_cross_densities=(2, 1, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0), actual_phase=3, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(2, 2, 2), global_aggregated_densities=(1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=3, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(2, 0, 2), global_aggregated_densities=(1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=0, phase_duration=0))
S1.append(LearningState(pre_cross_densities=(1, 0, 1), global_aggregated_densities=(1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=3, phase_duration=2))
S1.append(LearningState(pre_cross_densities=(2, 3, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 0.0, 1.0), actual_phase=0, phase_duration=0))
S1.append(LearningState(pre_cross_densities=(2, 2, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 0.0, 1.0), actual_phase=2, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(1, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 0.0, 1.0), actual_phase=0, phase_duration=0))
S1.append(LearningState(pre_cross_densities=(2, 3, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.0, 2.0), actual_phase=1, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(2, 0, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.0, 2.0), actual_phase=0, phase_duration=0))
S1.append(LearningState(pre_cross_densities=(1, 0, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.0, 2.0), actual_phase=1, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(1, 2, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0), actual_phase=0, phase_duration=0))
S1.append(LearningState(pre_cross_densities=(2, 1, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0), actual_phase=1, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(2, 0, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0), actual_phase=0, phase_duration=0))
S1.append(LearningState(pre_cross_densities=(1, 2, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=2, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(2, 0, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=0, phase_duration=0))
S1.append(LearningState(pre_cross_densities=(1, 1, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=2, phase_duration=1))
S1.append(LearningState(pre_cross_densities=(2, 2, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0), actual_phase=0, phase_duration=0))

S2=[]
S2.append(to_array(LearningState(pre_cross_densities=(2, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(0, 2, 2), global_aggregated_densities=(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 0, 1), global_aggregated_densities=(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(1, 2, 0), global_aggregated_densities=(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=2, phase_duration=1)))
S2.append(to_array(LearningState(pre_cross_densities=(1, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0), actual_phase=1, phase_duration=1)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 0, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0), actual_phase=2, phase_duration=1)))
S2.append(to_array(LearningState(pre_cross_densities=(1, 2, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(1, 1, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=1, phase_duration=2)))
S2.append(to_array(LearningState(pre_cross_densities=(1, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=2, phase_duration=2)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 1, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=3, phase_duration=1)))
S2.append(to_array(LearningState(pre_cross_densities=(1, 1, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=1, phase_duration=3)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 0, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 1, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 0, 3), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0), actual_phase=3, phase_duration=1)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0), actual_phase=2, phase_duration=1)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 0, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.0), actual_phase=3, phase_duration=1)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 0, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(1, 2, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.0), actual_phase=0, phase_duration=0)))
S2.append(to_array(LearningState(pre_cross_densities=(2, 2, 0), global_aggregated_densities=(1.0, 1.0, 2.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.0), actual_phase=3, phase_duration=2)))



S3=[]
S3.append(LearningState(pre_cross_densities=(2, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0), actual_phase=0, phase_duration=0))
S3.append(LearningState(pre_cross_densities=(1, 2, 2), global_aggregated_densities=(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=0, phase_duration=0))
S3.append(LearningState(pre_cross_densities=(2, 4, 1), global_aggregated_densities=(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=0, phase_duration=0))
S3.append(LearningState(pre_cross_densities=(2, 4, 1), global_aggregated_densities=(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=0, phase_duration=0))
S3.append(LearningState(pre_cross_densities=(1, 2, 0), global_aggregated_densities=(0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0), actual_phase=2, phase_duration=1))
S3.append(LearningState(pre_cross_densities=(1, 2, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0), actual_phase=1, phase_duration=1))
S3.append(LearningState(pre_cross_densities=(2, 0, 1), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0), actual_phase=2, phase_duration=1))
S3.append(LearningState(pre_cross_densities=(1, 2, 0), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0), actual_phase=0, phase_duration=0))
S3.append(LearningState(pre_cross_densities=(1, 1, 2), global_aggregated_densities=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=1, phase_duration=2))
S3.append(LearningState(pre_cross_densities=(500, 500, 500), global_aggregated_densities=(23.0, 25.0, 436.0, 44.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0), actual_phase=2, phase_duration=2))