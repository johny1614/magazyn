import time
from typing import List

import numpy as np

from StateMap import Cluster
from model import LearningState
from services.dist import dist_arr, dist

centroid = Cluster.get_radom_learning_state()
centroid_arr = centroid.to_array()
learningStates = [Cluster.get_radom_learning_state() for x in range(100000)]
timer_parsing=time.time()
learningStatesArray = [cluster.to_array() for cluster in learningStates]
timer_parsing=time.time()-timer_parsing
print(timer_parsing)

timer_arr = time.time()
for ls_array in learningStatesArray:
    a = dist_arr(centroid_arr, ls_array)
timer_arr = time.time() - timer_arr
print(timer_arr)


timer_ob = time.time()
for ls in learningStates:
    b = dist(centroid, ls)
timer_ob = time.time() - timer_ob
print(timer_ob)
