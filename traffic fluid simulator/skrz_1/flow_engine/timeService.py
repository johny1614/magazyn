import sys
sys.path.append("..")
from params.params import FlowParams
import numpy as np
class TimeService:
    time_range=np.arange(0,FlowParams.t_max,FlowParams.d_t)
    t_max=FlowParams.t_max
def time(self,index):
    return index*FlowParams.d_t
def getTimeIndex(time):
    return int(time/FlowParams.d_t)