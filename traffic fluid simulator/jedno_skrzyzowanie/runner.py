from beeprint import pp
from bokeh.layouts import column
import networkx as nx
from bokeh.models import Plot,Arrow,OpenHead, Range1d, Slider,MultiLine,Oval, Circle, HoverTool, BoxZoomTool, ResetTool,StaticLayoutProvider,NodesAndLinkedEdges
from bokeh.models.graphs import from_networkx
from bokeh.plotting import figure,curdoc
from utils.utils import edgeColor
from params.params import FlowParams,BokehParams
from pickle_loader import load_networks
from flow_engine.timeService import getTimeIndex
from flow_engine.network import NetworkLayout
import flow_engine.timeService as ts
def updateNodes(network):
    nodeCells=network.getAllCells()
    node_data=graph_renderer.node_renderer.data_source.data
    for v in range(len(nodeCells)):
        nodeCell=nodeCells[v]
        node_data['p'][v] = nodeCell.p
        if(nodeCell.p==FlowParams.p_max):
            print('v',v)
    graph_renderer.node_renderer.data_source.data=node_data    
def createTimeSlider():
    slider = Slider(start=BokehParams.Slider.start, end=BokehParams.Slider.end, value=0, step=FlowParams.d_t, title="Time")
    slider.on_change('value',onTimeChange)
    return slider
def onTimeChange(attr,old,time):
    time_index=getTimeIndex(time)
    actual_network=networks[time_index]
    updateNodes(actual_network)
    updateEdges()
    changeArrows()


def updateEdges():
    minLineWidth=BokehParams.Edge.minWidth
    maxLineWidth=BokehParams.Edge.maxWidth
    p_min=0
    p_max=FlowParams.p_max
    a=(maxLineWidth-minLineWidth)/(p_max-p_min)
    b=maxLineWidth-(maxLineWidth-minLineWidth)/(p_max-p_min)*p_max
    actualDenisties=graph_renderer.node_renderer.data_source.data['p']
    actualData=graph_renderer.edge_renderer.data_source.data
    licznik_pominietych=0 # ostatnie node'y nie maja edge'a wiec musimy je ignorowac!
    for i in range(len(actualDenisties)):
        if(i%(actualNetwork.cell_num-1)==0 and i!=1):
            licznik_pominietych=licznik_pominietych+1
        else:
            p=actualDenisties[i]
            line_width=a*p+b
            color=edgeColor(p)
            actualData["widths"][i-licznik_pominietych]=line_width
            actualData["colors"][i-licznik_pominietych]=color
    graph_renderer.edge_renderer.data_source.data = actualData
def createNodes(actualNetwork):
    nodeCellsEachRoad=[roadCells.normalGrid.cells for roadCells in actualNetwork.roads]
    all_members = set(range(sum(len(singleRoadCells) for singleRoadCells in nodeCellsEachRoad)))
    G.add_nodes_from(all_members)
    i=0
    for roadCells in nodeCellsEachRoad:# po kolei left,top,right,bottom roady
        for cell in roadCells:    
            G.nodes[i]['p'] = cell.p
            i=i+1
def createEdges(actualNetwork):
    global G
    nodeCellsEachRoad=[roadCells.normalGrid.cells for roadCells in actualNetwork.roads]
    for road in nodeCellsEachRoad:# po kolei left,top,right,bottom roady
        startNodes=road[:-1]
        endNodes=road[1:]
        for i in range(len(startNodes)):
            edgeTuple = [tuple([startNodes[i].number, endNodes[i].number])]
            G.add_edges_from(edgeTuple)
def style():
    global G
    zip_xy=zip(networkLayout.all_x,networkLayout.all_y)
    all_cells_numbers=actualNetwork.getAllCellsNumbers()
    graph_layout = dict(zip(all_cells_numbers, zip_xy)) # layout
    G.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    G.inspection_policy = NodesAndLinkedEdges()
    return graph_layout
def addArrows():
    global arrows
    edge_dispare=15
    leftArrows=[Arrow(name="arrow_0_straigth",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=-60, x_end=-30, y_start=-edge_dispare, y_end=-edge_dispare),Arrow(name="arrow_0_right",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=-40, x_end=-40,y_start=-edge_dispare,  y_end=-2*edge_dispare)]
    topArrows=[Arrow(name="arrow_1_straigth",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=-edge_dispare, x_end=-edge_dispare,y_start=60,  y_end=30),Arrow(name="arrow_1_right",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=-edge_dispare, x_end=-2*edge_dispare,y_start=40,  y_end=40)]
    rightArrows=[Arrow(name="arrow_2_straigth",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=60, x_end=30,y_start=edge_dispare,  y_end=edge_dispare),Arrow(name="arrow_2_right",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=40, x_end=40,y_start=edge_dispare,  y_end=2*edge_dispare)]
    bottomArrows=[Arrow(name="arrow_3_straigth",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=edge_dispare, x_end=edge_dispare,y_start=-60,  y_end=-30),Arrow(name="arrow_3_right",end=OpenHead(line_color="red", line_width=1,size=4),
                   x_start=edge_dispare, x_end=2*edge_dispare,y_start=-40,  y_end=-40)]
    arrows={"leftArrows":leftArrows,"topArrows":topArrows,"rightArrows":rightArrows,"bottomArrows":bottomArrows}
    for key in arrows.keys():
        plot.add_layout(arrows[key][0]) # szczalka prosto
        plot.add_layout(arrows[key][1]) # szczalka w prawo
def changeArrows():
    pp(plot.layout)
    arrowRenderers=[renderer for renderer in plot.renderers if(isinstance(renderer.name,str) and renderer.name.startswith("arrow"))]
    for arrowRenderer in arrowRenderers:
        arrowRenderer.end.line_color="green"
global G
global plot
global actualNetwork
networkLayout = NetworkLayout(cell_num=26,edge_dispare=15)
G = nx.Graph()
networks = load_networks()
actualNetwork=networks[0]
createNodes(actualNetwork)
createEdges(actualNetwork)
# Show with Bokeh
plot = Plot(plot_width=BokehParams.plot_width, plot_height=BokehParams.plot_height,
            x_range=Range1d(BokehParams.x_start,BokehParams.x_end), y_range=Range1d(BokehParams.y_start,BokehParams.y_end))
plot.title.text = "Graph Interaction Demonstration"

node_hover_tool = HoverTool(tooltips=[("index", "@index"),("p","@p"),("(x,y)", "($x, $y)")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
graph_layout=style()
edge_attrs={}
nodeCellsEachRoad=[roadCells.normalGrid.cells for roadCells in actualNetwork.roads]
leftCells=nodeCellsEachRoad[0]
graph_renderer = from_networkx(G, graph_layout, scale=1, center=(0, 0))
graph_renderer.node_renderer.glyph = Circle(size=6, fill_color="colors", line_width=1.0)
graph_renderer.node_renderer.data_source.data["colors"]=["red"]*len(G.nodes)

graph_renderer.edge_renderer.glyph = MultiLine(line_color="colors", line_alpha=0.8, line_width="widths")
graph_renderer.edge_renderer.data_source.data["colors"] = ["purple"] * len(G.edges)
graph_renderer.edge_renderer.data_source.data["widths"] = [2] * len(G.edges)
plot.renderers.append(graph_renderer)
addArrows()
slider = createTimeSlider()
curdoc().add_root(column(slider,plot))