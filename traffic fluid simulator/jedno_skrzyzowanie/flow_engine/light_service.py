from timeService import getTimeIndex
from enum import Enum
class Status(Enum):
    LIGHTING = 1
    PENDING_SWITCH = 2
class LightService:
    def __init__(self, epoch):
        self.epoch = epoch
        self.actual_green_roads = None
        self.switch_delay = 4
        self.switch_time_change_request = None
        self.status = Status.LIGHTING  #
        self.switch_time = None
    def processPending(self,time):
        if(self.status==Status.PENDING_SWITCH):
            if(self.time-self.switch_time_change_request>=self.switch_delay):
                self.status=Status.LIGHTING
                return True
        else:
            self.status=Status.PENDING_SWITCH
            self.switch_time_change_request=time
        return False
    def stayLights(self, time):
        for road in self.epoch.networks[getTimeIndex(time)].roads:
            if (road.name in self.actual_green_roads.road_names):
                road.light = 1
            else:
                road.light = 0
    def switchLights(self, time, green_light_phase):
        isSwitchable=self.processPending(time)
        if(isSwitchable):
            self.actual_green_roads = green_light_phase
            for road in self.epoch.networks[getTimeIndex(time)].roads:
                if (road.name in green_light_phase.road_names):
                    road.light = 1
                else:
                    road.light = 0
    def setInitialLights(self, green_light_phase):
        self.actual_green_roads = green_light_phase
        networkToInit = self.epoch.networks[0]  # od czasu 0 do switch delaya
        for road in networkToInit.roads:
            if (road.name in green_light_phase.road_names):
                road.light = 1
            else:
                road.light = 0
    def printLights(self):
        # print([road.name for road in self.actual_green_roads.roads])
        print(self.actual_green_roads.road_names)


class PhaseRoads:
    def __init__(self, number, road_names):
        self.road_names = road_names
        self.number = number
        self.light = None
