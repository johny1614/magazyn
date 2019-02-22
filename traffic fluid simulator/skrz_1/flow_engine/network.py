import sys

sys.path.append("..")
from params.params import FlowParams
from road import Road

class Network:
    def __init__(self, time):
        self.p_junction = 0
        self.time = time
        self.cell_num = 26
        self.roads = [Road(
            name="road-" + str(road_no),
            time=time,
            cell_index_start=road_no * self.cell_num)
            for road_no in range(3)]
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
        self.road_1_x = [(-cell_num + cell_no - 3) * FlowParams.d_x for cell_no in range(cell_num)]
        self.road_1_y = [-edge_dispare] * cell_num

        self.road_2_x = [-edge_dispare] * cell_num
        self.road_2_y = [(cell_num - cell_no + 3) * FlowParams.d_x for cell_no in range(cell_num)]

        self.road_3_x = [(cell_num - cell_no + 3) * FlowParams.d_x for cell_no in range(cell_num)]
        self.road_3_x = [edge_dispare] * cell_num
        self.all_x = self.road_1_x + self.road_2_x + self.road_3_x
        self.all_y = self.road_1_y + self.road_2_y + self.road_3_y
