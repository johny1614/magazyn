import sys

from network import Network

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
    ########## all centers
    for road_index in range(len(networks[time].roads)):
        grid_=networks[time].roads[road_index].grid
        prev_grid=networks[time-1].roads[road_index].grid
        # updating central cells
        for i in range(1, grid_.cells.__len__() - 1, 1):
            cell = grid_.cells[i]
            prev_cell_before = prev_grid.cells[i - 1]
            prev_cell = prev_grid.cells[i]
            prev_cell_after = prev_grid.cells[i + 1]
            cell.p = 0.5 * prev_cell.p + 0.25 * prev_cell_after.p + 0.25 * prev_cell_before.p + FlowParams.d_t / FlowParams.d_x / 2 * (
                        q(prev_cell_before.p) - q(prev_cell_after.p))
    # updating the first cell of road 3
    cell = networks[time].roads[2].grid.cells[0]
    prev_cell = networks[time-1].roads[2].grid.cells[0]
    prev_cell_after=networks[time-1].roads[2].grid.cells[1]
    cell_after=networks[time].roads[2].grid.cells[1]
    prev_lastCell_1=networks[time-1].roads[1].grid.cells[-1]
    cell.p = prev_cell.p-(cell_after.p-prev_cell_after.p)+1/2*prev_lastCell_1.p
    #updating the last cells of road 1
    lastCell = networks[time].roads[0].grid.cells[-1]
    prev_lastCell = networks[time-1].roads[0].grid.cells[-1]
    prev_lastCell_before=networks[time-1].roads[0].grid.cells[-1]
    lastCell_before=networks[time].roads[0].grid.cells[-1]
    lastCell.p=1/2*prev_lastCell.p+(prev_lastCell_before.p-lastCell_before.p)

    # updating the last cells of road 2
    lastCell = networks[time].roads[1].grid.cells[-1]
    prev_lastCell = networks[time - 1].roads[1].grid.cells[-1]
    prev_lastCell_before = networks[time - 1].roads[1].grid.cells[-1]
    lastCell_before = networks[time].roads[1].grid.cells[-1]
    lastCell.p = prev_lastCell.p + (prev_lastCell_before.p - lastCell_before.p)

def pickleNetworks():
    with open(r"../pickles/networks.pickle", "wb") as output_file:
        cPickle.dump(networks, output_file)
edgeName = "edge-1"
global networks
networks = [Network(time) for time in ts.time_range]
for network in networks:
    network.roads[0].grid.cells[0].p=FlowParams.p_1_source
    network.roads[1].grid.cells[0].p=FlowParams.p_2_source
for time in ts.time_range[1:]: # we skip time =0
    calculateDensities(time)
pickleNetworks()
