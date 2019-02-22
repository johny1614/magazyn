import sys
sys.path.append("..")
# sys.path.append('c:\\Users\\johny\\Desktop\\magisterka\\traffic fluid simulator\\single_junction')
from params.params import FlowParams
import cPickle
import numpy as np
from grid import Grid as Grid
from utils.utils import q,gamma_wylot_
from timeService import TimeService as ts
from timeService import getTimeIndex,time

def printGrids():
    global grids
    for timeIndex in range(len(grids)):
        time_=timeIndex*FlowParams.d_t
        print("time:",time_)
        grid=grids[timeIndex]
        grid.normalGrid.print_p()
        grid.stagerredGrid.print_p()
def calculateDensities(time):
    grid=grids[time]
    prev_grid=grids[time-1]
    # updating the first cell
    firstCell = grid.cells[0]
    prev_firstCell = prev_grid.cells[0]
    prev_firstCell_after = prev_grid.cells[1]
    firstCell.p = 0.5*prev_firstCell.p+0.25*prev_firstCell_after.p+0.25*FlowParams.p_source+FlowParams.d_t/FlowParams.d_x/2*(q(FlowParams.p_source)-q(prev_firstCell_after.p))
    # updating central cells
    for i in range(1,grid.cells.__len__()-1,1):
        cell=grid.cells[i]
        prev_cell_before=prev_grid.cells[i-1]
        prev_cell=prev_grid.cells[i]
        prev_cell_after=prev_grid.cells[i+1]
        cell.p=0.5*prev_cell.p+0.25*prev_cell_after.p+0.25*prev_cell_before.p+FlowParams.d_t/FlowParams.d_x/2*(q(prev_cell_before.p)-q(prev_cell_after.p))
    #updating the last cell
    lastCell = grid.cells[-1]
    prev_lastCell = prev_grid.cells[-1]
    prev_lastCell_before = prev_grid.cells[-2]
    p_out=0
    lastCell.p=0.5*prev_lastCell.p+0.25*p_out+0.25*prev_lastCell_before.p+FlowParams.d_t/FlowParams.d_x/2*(q(prev_lastCell_before.p)-q(p_out))

def pickleGrids():
    global grids
    with open(r"../pickles/grids.pickle", "wb") as output_file:
        cPickle.dump(grids, output_file)
edgeName = "edge-1"
global grids
grids = [Grid(edgeName,time) for time in ts.time_range]
for time in ts.time_range[1:]: # we skip time =0
    calculateDensities(time)
pickleGrids()
