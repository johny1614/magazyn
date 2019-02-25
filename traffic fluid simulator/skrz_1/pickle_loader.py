import sys
import dill
from flow_engine import road,network,light_service,epoch
sys.modules['network']=network
sys.modules['road']=road
sys.modules['epoch']=epoch
sys.modules['light_service']=light_service

def load_networks():
    with open(r"pickles/networks.pickle", "rb") as input_file:
        e = dill.load(input_file)
        return e
def load_epoch(name="epoch"):
    with open(r"pickles/"+name+".pickle", "rb") as input_file:
        e = dill.load(input_file)
        return e

