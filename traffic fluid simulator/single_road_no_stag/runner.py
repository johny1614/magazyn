import sys
from bokeh.layouts import column
from tempfile import mkstemp
import networkx as nx
from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, Slider,MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool,StaticLayoutProvider,NodesAndLinkedEdges
from bokeh.models.graphs import from_networkx
from bokeh.plotting import figure,curdoc

from bokeh.palettes import Spectral4
from params.params import FlowParams,BokehParams
from utils.utils import edgeColor
from params.params import FlowParams,BokehParams
from pickle_loader import loadGrids
from flow_engine.timeService import getTimeIndex
def createNodes(grid):
    global G
    nodeCells=grid.cells
    all_members = set(range(len(nodeCells)))
    G.add_nodes_from(all_members)
    for v in G:
        nodeCell=nodeCells[v]
        G.nodes[v]['p'] = nodeCell.p
def updateNodes(grid):
    nodeCells=grid.cells #global
    actualData=graph_renderer.node_renderer.data_source.data
    for v in range(len(nodeCells)):
        nodeCell=nodeCells[v]
        actualData['p'][v] = nodeCell.p
    graph_renderer.node_renderer.data_source.data=actualData    
def createEdges():
    global G
    startEdges=[cell.number for cell in nodeCells[:-1]]
    endEdges=[cell.number for cell in nodeCells[1:]]
    for i in range(len(startEdges)):
        G.add_edges_from([tuple([startEdges[i],endEdges[i]])])
def createTimeSlider():
    title="Time"
    slider = Slider(start=BokehParams.Slider.start, end=BokehParams.Slider.end, value=0, step=FlowParams.d_t, title=title) # objekt slidera
    slider.on_change('value',onTimeChange)
    return slider
def style():
    global G
    global node_indices,plot
    x=[cell_no*FlowParams.d_x for cell_no in range(len(nodeCells))]
    y=[0]*len(nodeCells)
    nodeCellNumbers=[cell.number for cell in nodeCells]
    zip_xy=zip(x, y)
    nodecellsNumber=[x.number for x in nodeCells]
    graph_layout = dict(zip(nodecellsNumber, zip_xy)) # layout
    G.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    G.inspection_policy = NodesAndLinkedEdges()
    return graph_layout
def onTimeChange(attr,old,time):
    timeIndex_=getTimeIndex(time)
    grid=grids[timeIndex_]
    updateNodes(grid)
    updateEdges(grid)
def updateEdges(grid):
    minLineWidth=BokehParams.Edge.minWidth
    maxLineWidth=BokehParams.Edge.maxWidth
    p_min=0
    p_max=FlowParams.p_max
    #  w przyszlosci zamiast time - bedzie gestosc
    a=(maxLineWidth-minLineWidth)/(p_max-p_min)
    b=maxLineWidth-(maxLineWidth-minLineWidth)/(p_max-p_min)*p_max
    actualDenisties=graph_renderer.node_renderer.data_source.data['p']
    actualData=graph_renderer.edge_renderer.data_source.data
    for i in range(len(actualDenisties)-1):
        p=actualDenisties[i]
        line_width=a*p+b
        color=edgeColor(p)
        actualData["widths"][i]=line_width
        actualData["colors"][i]=color
    graph_renderer.edge_renderer.data_source.data = actualData
global G
global grid
grids=loadGrids()
timeIndex_=5
grid=grids[timeIndex_]
nodeCells=grids[timeIndex_].cells #global
G = nx.Graph()
createNodes(grid)
createEdges()
# Show with Bokeh
plot = Plot(plot_width=1600, plot_height=1000,
            x_range=Range1d(-2, 1002), y_range=Range1d(-5, 5))
plot.title.text = "Graph Interaction Demonstration"

node_hover_tool = HoverTool(tooltips=[("index", "@index"),("p","@p")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

graph_layout=style()
edge_attrs={}

graph_renderer = from_networkx(G, graph_layout, scale=1, center=(0, 0))

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="colors", line_width=1.0)
graph_renderer.node_renderer.data_source.data["colors"] = ["red"]*len(nodeCells)

graph_renderer.edge_renderer.glyph = MultiLine(line_color="colors", line_alpha=0.8, line_width="widths")
graph_renderer.edge_renderer.data_source.data["colors"] = ["purple"] * (len(nodeCells)-1)
graph_renderer.edge_renderer.data_source.data["widths"] = [2] * (len(nodeCells)-1)

plot.renderers.append(graph_renderer)
slider = createTimeSlider()
curdoc().add_root(column(slider,plot))