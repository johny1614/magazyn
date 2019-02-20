from params import Params
from utils import q,positive
class Grid:
    def __init__(self,edge,time):
        self.time=time
        self.stagerredGrid = StageredGrid()
        self.normalGrid = NormalGrid()
    def updateQ(self):
        for cell in self.stagerredGrid.cells:
            cell.q=cell.p*(1-cell.p/Params.p_max)*Params.v_max
        for cell in self.normalGrid.cells:
            cell.q=cell.p*(1-cell.p/Params.p_max)*Params.v_max
    def positiveDensity(self):
        for cell in self.stagerredGrid.cells:
            cell.p=cell.p if cell.p>0 else 0
        for cell in self.normalGrid.cells:
            cell.p=cell.p if cell.p>0 else 0
    def updateNormalGrid(self): # basing on stagerred one
        for cell_no in range(len(self.normalGrid.cells)):
            cell = self.normalGrid.cells[cell_no]
            if(cell_no==0):
                cell.p=self.stagerredGrid.cells[0].p
            elif(cell_no==len(self.normalGrid.cells)-1):
                cell.p=self.stagerredGrid.cells[len(self.normalGrid.cells)].p
            else:
                previousCell=self.normalGrid.cells[cell_no-1]
                cell.p=self.stagerredGrid.cells[cell_no].p-previousCell.p
        self.normalGrid.print_p()
        self.normalGrid.updateQ()
class StageredGrid:
    def __init__(self):
        self.numberOfCells=Params.x_max/Params.d_x/2+2
        self.cells=[Cell() for cell in range(self.numberOfCells)]
        self.time=0
    def print_p(self):
        print([cell.p for cell in self.cells])
    def updateQ(self):
        for cell in self.cells:
            cell.q=cell.p*(1-cell.p/Params.p_max)*Params.v_max
class NormalGrid:
    def __init__(self):
        self.numberOfCells=Params.x_max/Params.d_x/2+1
        self.cells=[Cell() for cell in range(self.numberOfCells)]
        self.time=0
    def print_p(self):
        print([cell.p for cell in self.cells])
    def updateQ(self):
        for cell in self.cells:
            cell.q=cell.p*(1-cell.p/Params.p_max)*Params.v_max
class Cell(object):
    def __init__(self):       
        self._p=Params.p_init
        self._q=Params.q_init if Params.q_init else q(Params.p_init) 
    @property
    def p(self):
        return self._p
    @p.setter
    def p(self, value):
        self._p = positive(value)
        self.q = positive(q(value))
    @property
    def q(self):
        return self._q
    @q.setter
    def q(self, value):
        self._q = positive(value)
