import sys
import dill
from flow_engine import grid 
sys.modules['grid']=grid
def loadGrids():
    with open(r"pickles/grids.pickle", "rb") as input_file:
        e = dill.load(input_file)
        return e