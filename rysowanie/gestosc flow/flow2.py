import numpy as np
from params import Params
from grid import Grid
from utils import q,gamma_wylot_
from timeService import TimeService as ts
from timeService import timeIndex,time
def updateNormalGrid(time):
    global grids
    grid=grids[timeIndex(time)]
    for cell_no in range(len(grid.normalGrid.cells)):
        cell=grid.normalGrid.cells[cell_no]
        pnk=grid.stagerredGrid.cells[cell_no].p
        pnk_plus_one=grid.stagerredGrid.cells[cell_no+1].p
        cell.p=(pnk+pnk_plus_one)/2
def stagerredUpdate(time):
    global grids
    grid=grids[timeIndex(time)]
    previousGrid=grids[timeIndex(time)-1]
    for cell_no in range(len(grid.stagerredGrid.cells)):
        # updatujemy p oraz q tylko dla stagerred
        cell=grid.stagerredGrid.cells[cell_no]
        cell_t__1=previousGrid.stagerredGrid.cells[cell_no]
        if(cell_no==0):
            qk0=previousGrid.normalGrid.cells[cell_no].q
            cell.p=cell_t__1.p-2*(Params.d_t/Params.d_x)*(qk0-gamma_wlot)
        elif(cell_no==len(grid.stagerredGrid.cells)-1):
            # gamma_wylot=grid.normalGrid.cells[grid.normalGrid.numberOfCells-1].q
            qkl=previousGrid.normalGrid.cells[cell_no-1].q
            gamma_wylot=gamma_wylot_(previousGrid.normalGrid.cells[-1].p)
            #TODO tutaj uwzglednic swiatla
            cell.p=cell_t__1.p-2*(Params.d_t/Params.d_x)*(gamma_wylot-qkl)
        else:
            qkn=previousGrid.normalGrid.cells[cell_no].q
            qkn__1=previousGrid.normalGrid.cells[cell_no-1].q
            cell.p=cell_t__1.p-(Params.d_t/Params.d_x)*(qkn-qkn__1)
def printGrids():
    global grids
    for timeIndex in range(len(grids)):
        time_=timeIndex*Params.d_t
        print("time:",time_)
        grid=grids[timeIndex]
        grid.normalGrid.print_p()
        grid.stagerredGrid.print_p()
edgeName = "edge-1"
global grids
grids = [Grid(edgeName,time) for time in ts.time_range]
gamma_wlot=1.2
# gamma_wylot=2.0625
for time in ts.time_range[1:]: # we skip time =0
    print(time) #tutaj time  to jest t+1 z pracy
    stagerredUpdate(time)
    updateNormalGrid(time)    
printGrids()



             

#     grid.normalGrid.print_p()
#     for cell_no in range(len(grid.stagerredGrid.cells)):
#         cell=grid.stagerredGrid.cells[cell_no]
#         if(cell_no==0):
#             qtk=grid.normalGrid.cells[cell_no].q
#             cell.p=cell.p-Params.d_t/Params.d_x*(qtk-gamma_wlot)
#         elif(cell_no==len(grid.stagerredGrid.cells)-1):
#             # gamma_wylot=grid.normalGrid.cells[grid.normalGrid.numberOfCells-1].q
#             qtk__1=grid.normalGrid.cells[cell_no-1].q
#             #TODO tutaj uwzglednic swiatla
#             cell.p=cell.p-Params.d_t/Params.d_x*(qtk-qtk__1)
#         else:
#             cell.p=cell.p-Params.d_t/Params.d_x/2*(qtk-gamma_wlot)
#     grid.positiveDensity()
#     grid.updateQ()
#     grid.updateNormalGrid()

