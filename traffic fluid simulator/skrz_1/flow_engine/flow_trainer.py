from network import Network
from timeService import TimeService as TS
from epoch import Epoch
import flow
networks = [Network(time) for time in TS.time_range]
epoch = Epoch(networks,"eposzek")
flow.simulate(epoch,True)
epoch.rate()
