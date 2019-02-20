import sys

sys.path.append("..")
from road_grid import Road
from params.params import FlowParams
from road_grid import Road
from light_service import PhaseRoads


class Network:
    def __init__(self, time):
        self.time = time
        self.cell_num = 26
        roads = [Road("road-" + str(road_no), time, road_no * self.cell_num, "outside", "junction") for road_no in
                 range(4)]
        q_flow_input = [[0.5] * self.cell_num] * 4
        reverseRoads = [Road("road-rev-" + str(road_no), time, road_no * self.cell_num, "junction", "outside") for
                        road_no in range(4, 8)]
        self.roads = roads + reverseRoads
        self.phaseRoads = [PhaseRoads(0, [roads[0].name, roads[2].name]), PhaseRoads(1, [roads[1].name, roads[3].name])]

    def getAllCellsNumbers(self):
        all_cells_numbers = []
        roadCells = [road.normalGrid.cells for road in [road for road in self.roads]]
        for road in roadCells:
            for cell in road:
                all_cells_numbers.append(cell.number)
        return all_cells_numbers

    def getAllCells(self):
        all_cells = []
        roadCells = [road.normalGrid.cells for road in [road for road in self.roads]]
        for road in roadCells:
            for cell in road:
                all_cells.append(cell)
        return all_cells


class NetworkLayout:
    def __init__(self, cell_num, edge_dispare):
        self.leftRoad_x = [(-cell_num + cell_no - 3) * FlowParams.d_x for cell_no in range(cell_num)]
        self.leftRoad_y = [-edge_dispare] * cell_num

        self.topRoad_x = [-edge_dispare] * cell_num
        self.topRoad_y = [(cell_num - cell_no + 3) * FlowParams.d_x for cell_no in range(cell_num)]

        self.rightRoad_x = [(cell_num - cell_no + 3) * FlowParams.d_x for cell_no in range(cell_num)]
        self.rightRoad_y = [edge_dispare] * cell_num

        self.bottomRoad_x = [edge_dispare] * cell_num
        self.bottomRoad_y = [(-cell_num + cell_no - 3) * FlowParams.d_x for cell_no in range(cell_num)]

        self.leftRoad_x_re = [-(cell_no + 4) * FlowParams.d_x for cell_no in range(cell_num)]
        self.leftRoad_y_re = [+edge_dispare] * cell_num

        self.topRoad_x_re = [edge_dispare] * cell_num
        self.topRoad_y_re = [(cell_no + 4) * FlowParams.d_x for cell_no in range(cell_num)]

        self.rightRoad_x_re = [(cell_no + 4) * FlowParams.d_x for cell_no in range(cell_num)]
        self.rightRoad_y_re = [-edge_dispare] * cell_num

        self.bottomRoad_x_re = [-edge_dispare] * cell_num
        self.bottomRoad_y_re = [-(cell_no + 4) * FlowParams.d_x for cell_no in range(cell_num)]

        self.all_x = self.leftRoad_x + self.topRoad_x + self.rightRoad_x + self.bottomRoad_x + self.leftRoad_x_re + self.topRoad_x_re + self.rightRoad_x_re + self.bottomRoad_x_re
        self.all_y = self.leftRoad_y + self.topRoad_y + self.rightRoad_y + self.bottomRoad_y + self.leftRoad_y_re + self.topRoad_y_re + self.rightRoad_y_re + self.bottomRoad_y_re
