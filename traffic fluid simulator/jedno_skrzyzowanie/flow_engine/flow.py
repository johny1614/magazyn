import sys
sys.path.append("..")
from params.params import FlowParams
import cPickle
from utils.utils import q, gamma_wylot_
from timeService import TimeService as ts
from timeService import getTimeIndex
from TURN_TABLE import TurnTable


def __updateNormalGrid(time):
    global networks
    network = networks[getTimeIndex(time)]
    for road in network.roads:
        for cell_no in range(len(road.normalGrid.cells)):
            cell = road.normalGrid.cells[cell_no]
            pnk = road.stagerredGrid.cells[cell_no].p
            pnk_plus_one = road.stagerredGrid.cells[cell_no + 1].p
            cell.p = (pnk + pnk_plus_one) / 2


def __get_junction_flow(road_index, prev_network):
    incomes = [row for row in TurnTable.flow_probability if (row[1] == road_index and row[2] > 0)]
    flow = 0
    for incomeRow in incomes:
        incomeRoad = prev_network.roads[incomeRow[0]]
        incomeFlow = incomeRoad.normalGrid.cells[-1].q * incomeRow[2]
        flow += incomeFlow
    return flow

def __stagerredUpdate(time):
    # prefix prev odnosi sie do obiektu w czasie t-1
    # posfix before odnosi sie do komorki w miejscu n-1
    # postfic next odnosi sie do komorki w miejscu n+1
    global networks
    network = networks[getTimeIndex(time)]
    prev_network = networks[getTimeIndex(time) - 1]
    for road_index in range(len(network.roads)):
        road = network.roads[road_index]
        prev_road = prev_network.roads[road_index]
        for cell_no in range(len(road.stagerredGrid.cells)):
            # updatujemy p tylko dla stagerred (q sie z automatu updejtuje w setterze p)
            cell = road.stagerredGrid.cells[cell_no]
            prev_cell = prev_road.stagerredGrid.cells[cell_no]
            if (cell_no == 0):
                qk0 = prev_road.normalGrid.cells[cell_no].q
                if (road.flow_input_type == 'outside'):
                    input_flow = road.input_flow[getTimeIndex(time)][road_index]
                    cell.p = prev_cell.p - 2 * (FlowParams.d_t / FlowParams.d_x) * (qk0 - input_flow)
                else:  # t.j. junction jest zrodlem
                    input_flow = __get_junction_flow(road_index, prev_network)
                    cell.p = prev_cell.p - 2 * (FlowParams.d_t / FlowParams.d_x) * (qk0 - input_flow)
            elif (cell_no == len(road.stagerredGrid.cells) - 1):
                qkl = prev_road.normalGrid.cells[cell_no - 1].q
                light = 1 if road.flow_output_type == "outside" else road.light
                gamma_wylot = gamma_wylot_(prev_road.normalGrid.cells[-1].p) * light
                cell.p = prev_cell.p - 2 * (FlowParams.d_t / FlowParams.d_x) * (gamma_wylot - qkl)
            else:
                prev_q = prev_road.normalGrid.cells[cell_no].q
                prev_q_before = prev_road.normalGrid.cells[cell_no - 1].q
                cell.p = prev_cell.p - (FlowParams.d_t / FlowParams.d_x) * (prev_q - prev_q_before)


def __pickleEpoch(epoch):
    with open(r"../pickles/"+epoch.name+".pickle", "wb") as output_file:
        cPickle.dump(epoch, output_file)

def simulate(epoch,do_pickle):
    global networks
    networks = epoch.networks
    epoch.light_service.setInitialLights(networks[0].phaseRoads[0])
    for time in ts.time_range[1:-1]:  # we skip time =0 and t-1
        if (time % 7 == 1):
            zeroPhaseRoads = networks[getTimeIndex(time)].phaseRoads[0]
            epoch.light_service.switchLights(time, zeroPhaseRoads)
        elif (time % 23 == 1):
            firstPhaseRoads = networks[getTimeIndex(time)].phaseRoads[1]
            epoch.light_service.switchLights(time, firstPhaseRoads)
        elif (time != ts.time_range[-1] and time != 0):
            epoch.light_service.stayLights(time)
        __stagerredUpdate(time)
        __updateNormalGrid(time)
    if(do_pickle):
        __pickleEpoch(epoch)
