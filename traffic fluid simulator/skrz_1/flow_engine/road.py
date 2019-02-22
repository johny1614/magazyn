import os.path as path, sys
from flow_engine.grid import Grid
sys.path.append("..")
from params.params import FlowParams
from utils.utils import q,positive
from timeService import TimeService as ts
class Road:
    def __init__(self, name, time,cell_index_start):
        self.name = name
        self.time=time
        self.cell_index_start=cell_index_start
        self.grid = Grid()
        self.turn_probability = {'right':0,'straight':0,'left':0}
        self.light=0
        self.input_flow = [[0.6]*4]*len(ts.time_range)
