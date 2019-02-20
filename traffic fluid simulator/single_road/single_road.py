from bokeh.layouts import column
from functools import partial
from bokeh.io import show, output_file
from bokeh.plotting import figure,curdoc
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval,MultiLine,HoverTool,Slider
from bokeh.palettes import Spectral3
from bokeh.models.graphs import NodesAndLinkedEdges
from params.params import FlowParams,BokehParams
from utils.utils import edgeColor
from pickle_loader import loadGrids
def style(graph):
    global node_indices,plot
    graph.node_renderer.data_source.add(["#99d594"]*(len(node_indices)), 'color') # kolory node'ow
    graph.node_renderer.glyph = Oval(height=BokehParams.point_height, width=BokehParams.point_width, fill_color='color') # ksztalt node'a
    graph_layout = dict(zip(node_indices, zip(x, y))) # layout
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    graph.inspection_policy = NodesAndLinkedEdges()
def onTimeChange(attr,old,time):
    global graph
    global edges
    minLineWidth=BokehParams.Edge.minWidth
    maxLineWidth=BokehParams.Edge.maxWidth
    timeStart=BokehParams.Slider.start
    timeEnd=BokehParams.Slider.end
    #  w przyszlosci zamiast time - bedzie gestosc
    a=(maxLineWidth-minLineWidth)/(timeEnd-timeStart)
    b=maxLineWidth-(maxLineWidth-minLineWidth)/(timeEnd-timeStart)*timeEnd
    line_width=a*time+b
    edges["line_width"]=[line_width]*(len(node_indices)-1)
    edges["line_color"]=[edgeColor(line_width,min_p=0=minLineWidth,MAX_width=maxLineWidth)]*(len(node_indices)-1)
    graph.edge_renderer.data_source.data =edges 

def createTimeSlider():
    title="Time"
    slider = Slider(start=0, end=FlowParams.t_max, value=0, step=FlowParams.d_t, title=title) # objekt slidera
    slider.on_change('value',onTimeChange)
    return slider
grids=loadGrids()
grid=grids[15]
x=[cell_no*FlowParams.d_x for cell_no in range(len(grid.normalGrid.cells))]
# x=[0,5] # wyswietlane wspolrzedne  x node'ow 
y=[0]*len(x) # wyswietlane wspolrzedne  y node'ow 
node_indices=[cell.number for cell in grid.normalGrid.cells]
tooltips = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
]

plot = figure(title='Graph Layout Demonstration', x_range=BokehParams.x_range, y_range=BokehParams.y_range,
              tools='', toolbar_location=None,tooltips=tooltips)
graph = GraphRenderer()
graph.node_renderer.data_source.add(node_indices, 'index') # indeksy node'ow

startEdges=node_indices[:-1]
endEdges=node_indices[1:]
edges=dict( # datasource dla edge'y odpowiedzialne za polaczenia - bez nich mamy same kropki
    start=startEdges,
    end=endEdges) # we dont make edge from center to center
edges["line_width"]=[2]*len(startEdges)
graph.edge_renderer.glyph.line_width = {'field': 'line_width'}
edges["line_color"]=["rgb(0,255,0)"]*(len(startEdges))
graph.edge_renderer.glyph.line_color = {'field': 'line_color'}
graph.edge_renderer.data_source.data =edges 
style(graph)
plot.renderers.append(graph)
plot.add_tools(HoverTool(tooltips="index: @index"))
slider=createTimeSlider()
curdoc().add_root(column(slider,plot))
# awdsad