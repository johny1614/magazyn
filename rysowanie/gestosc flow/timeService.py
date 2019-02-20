import numpy as np
from params import Params
class TimeService:
    time_range=np.arange(0,Params.t_max,Params.d_t)
    t_max=Params.t_max
def time(self,index):
    return index*Params.d_t
def timeIndex(time):
    return int(time/Params.d_t)