import os.path as path, sys
sys.path.append("..")
from params.params import FlowParams
from utils.utils import q,positive
class Grid:
    def __init__(self):
        self.numberOfCells = int(FlowParams.x_max / FlowParams.d_x + 1)
        self.cells = [Cell(cell_no) for cell_no in range(self.numberOfCells)]
        # self.time = time
    def updateQ(self):
        for cell in self.normalGrid.cells:
            cell.q=cell.p*(1-cell.p/FlowParams.p_max)*FlowParams.v_max
    def positiveDensity(self):
        for cell in self.normalGrid.cells:
            cell.p=cell.p if cell.p>0 else 0
    def print_p(self):
        print([cell.p for cell in self.cells])
    def updateQ(self):
        for cell in self.cells:
            cell.q = cell.p * (1 - cell.p / FlowParams.p_max) * FlowParams.v_max
class Cell(object):
    def __init__(self,number):
        self.number=number
        self._p=FlowParams.p_init
        self._q=FlowParams.q_init if FlowParams.q_init else q(FlowParams.p_init) 
    @property
    def p(self):
        return self._p
    @p.setter
    def p(self, value):
        self._p = min([positive(value),FlowParams.p_max])
        self.q = positive(q(self._p))
    @property
    def q(self):
        return self._q
    @q.setter
    def q(self, value):
        self._q = positive(value)
