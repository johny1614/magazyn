from bokeh.layouts import column
from functools import partial
from bokeh.io import show, output_file
from bokeh.plotting import figure,curdoc
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval,MultiLine,HoverTool,Slider
from bokeh.palettes import Spectral5
from bokeh.models.graphs import NodesAndLinkedEdges
from utils.utils import edgeColor
from config import Config

def style(graph):
    global node_indices,plot
    graph.node_renderer.data_source.add(Spectral5, 'color') # kolory node'ow
    graph.node_renderer.glyph = Oval(height=0.6, width=0.6, fill_color='color') # ksztalt node'a
    graph_layout = dict(zip(node_indices, zip(x, y))) # layout
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    graph.inspection_policy = NodesAndLinkedEdges()
def onTimeChange(attr,old,time):
    global graph
    global edges
    minLineWidth=Config.Edge.minWidth
    maxLineWidth=Config.Edge.maxWidth
    timeStart=Config.Slider.start
    timeEnd=Config.Slider.end
    #  w przyszlosci zamiast time - bedzie gestosc
    a=(maxLineWidth-minLineWidth)/(timeEnd-timeStart)
    b=maxLineWidth-(maxLineWidth-minLineWidth)/(timeEnd-timeStart)*timeEnd
    line_width=a*time+b
    edges["line_width"]=[line_width]*4
    edges["line_color"]=[edgeColor(line_width,min_p=0=minLineWidth,MAX_width=maxLineWidth)]*4
    graph.edge_renderer.data_source.data =edges 

def createTimeSlider():
    title="Time"
    slider = Slider(start=Config.Slider.start, end=Config.Slider.end, value=0, step=.1, title=title) # objekt slidera
    slider.on_change('value',onTimeChange)
    return slider
x=[0,5,0,-5,0] # wyswietlane wspolrzedne  x node'ow 
y=[5,0,-5,0,0] # wyswietlane wspolrzedne  y node'ow 
node_indices=['top','right','bottom','left','center']
plot = figure(title='Graph Layout Demonstration', x_range=(-6,6), y_range=(-6,6),
              tools='', toolbar_location=None)
graph = GraphRenderer()
graph.node_renderer.data_source.add(node_indices, 'index') # indeksy node'ow
edges=dict( # datasource dla edge'y odpowiedzialne za polaczenia - bez nich mamy same kropki
    start=['center']*(len(node_indices)-1),
    end=node_indices[:-1]) # we dont make edge from center to center
edges["line_width"]=[2,2,2,2]
graph.edge_renderer.glyph.line_width = {'field': 'line_width'}
edges["line_color"]=["rgb(0,255,0)"]*4
graph.edge_renderer.glyph.line_color = {'field': 'line_color'}
graph.edge_renderer.data_source.data =edges 
style(graph)
plot.renderers.append(graph)
slider=createTimeSlider()
curdoc().add_root(column(slider,plot))
# curdoc().add_root(column(slider))