import sys

sys.path.append("..")
from params.params import FlowParams
from road import Road

class Network:
    def __init__(self, time):
        self.p_junction = 0
        self.time = time
        self.cell_num = int(FlowParams.x_max / FlowParams.d_x + 1)
        self.roads = [Road(
            name="road-" + str(road_no),
            time=time,
            cell_index_start=road_no * self.cell_num)
            for road_no in range(3)]
    def getAllCellsNumbers(self):
        all_cells_numbers = []
        roadCells = [road.grid.cells for road in [road for road in self.roads]]
        for road in roadCells:
            for cell in road:
                all_cells_numbers.append(cell.number)
        return all_cells_numbers
    def getAllCells(self):
        all_cells = []
        roadCells = [road.grid.cells for road in [road for road in self.roads]]
        for road in roadCells:
            for cell in road:
                all_cells.append(cell)
        return all_cells

class NetworkLayout:
    def __init__(self):
        cell_nums = range(int(FlowParams.x_max / FlowParams.d_x + 1))
        self.road_1_x = [x*50 for x in cell_nums]
        self.road_1_y = [-40*x+40*len(cell_nums) for x in cell_nums]

        self.road_2_x = [x*50 for x in cell_nums]
        self.road_2_y = [40*x-40*len(cell_nums) for x in cell_nums]

        self.road_3_x = [600+40*x for x in cell_nums]
        self.road_3_y = [0]*len(cell_nums)
        self.all_x = self.road_1_x + self.road_2_x + self.road_3_x
        self.all_y = self.road_1_y + self.road_2_y + self.road_3_y
        print('all_x',self.all_x)
        print('all_y',self.all_y)

