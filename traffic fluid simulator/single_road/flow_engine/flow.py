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

def updateNormalGrid(time):
    global grids
    grid=grids[getTimeIndex(time)]
    for cell_no in range(len(grid.normalGrid.cells)):
        cell=grid.normalGrid.cells[cell_no]
        pnk=grid.stagerredGrid.cells[cell_no].p
        pnk_plus_one=grid.stagerredGrid.cells[cell_no+1].p
        cell.p=(pnk+pnk_plus_one)/2
def stagerredUpdate(time):
    global grids
    grid=grids[getTimeIndex(time)]
    previousGrid=grids[getTimeIndex(time)-1]
    for cell_no in range(len(grid.stagerredGrid.cells)):
        # updatujemy p oraz q tylko dla stagerred
        cell=grid.stagerredGrid.cells[cell_no]
        cell_t__1=previousGrid.stagerredGrid.cells[cell_no]
        if(cell_no==0):
            qk0=previousGrid.normalGrid.cells[cell_no].q
            cell.p=cell_t__1.p-2*(FlowParams.d_t/FlowParams.d_x)*(qk0-gamma_wlot)
        elif(cell_no==len(grid.stagerredGrid.cells)-1):
            # gamma_wylot=grid.normalGrid.cells[grid.normalGrid.numberOfCells-1].q
            qkl=previousGrid.normalGrid.cells[cell_no-1].q
            gamma_wylot=gamma_wylot_(previousGrid.normalGrid.cells[-1].p)
            #TODO tutaj uwzglednic swiatla
            cell.p=cell_t__1.p-2*(FlowParams.d_t/FlowParams.d_x)*(gamma_wylot-qkl)
        else:
            qkn=previousGrid.normalGrid.cells[cell_no].q
            qkn__1=previousGrid.normalGrid.cells[cell_no-1].q
            cell.p=cell_t__1.p-(FlowParams.d_t/FlowParams.d_x)*(qkn-qkn__1)
def printGrids():
    global grids
    for timeIndex in range(len(grids)):
        time_=timeIndex*FlowParams.d_t
        print("time:",time_)
        grid=grids[timeIndex]
        grid.normalGrid.print_p()
        grid.stagerredGrid.print_p()
def pickleGrids():
    global grids
    with open(r"../pickles/grids.pickle", "wb") as output_file:
        cPickle.dump(grids, output_file)
edgeName = "edge-1"
global grids
grids = [Grid(edgeName,time) for time in ts.time_range]
gamma_wlot=1.2
for time in ts.time_range[1:]: # we skip time =0
    stagerredUpdate(time)
    updateNormalGrid(time)    
pickleGrids()


