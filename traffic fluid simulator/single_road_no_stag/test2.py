"""
Zachary's Karate Club graph
Data file from:
http://vlado.fmf.uni-lj.si/pub/networks/data/Ucinet/UciData.htm
Reference:
Zachary W. (1977).
An information flow model for conflict and fission in small groups.
Journal of Anthropological Research, 33, 452-473.
"""

import networkx as nx
import random

from bokeh.io import show, curdoc
from bokeh.layouts import Column
from bokeh.models import Plot, Range1d, MultiLine, Circle
from bokeh.models.graphs import from_networkx
from bokeh.models.widgets import Button
from bokeh.palettes import Spectral4, Spectral10

L = 78

G=nx.karate_club_graph()

N = nx.number_of_nodes(G)

plot = Plot(plot_width=400, plot_height=400,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))

graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0,0))

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="colors", line_width=1.0)
graph_renderer.node_renderer.data_source.data["colors"] = [Spectral4[0] ]* N

graph_renderer.edge_renderer.glyph = MultiLine(line_color="colors", line_alpha=0.8, line_width="widths")

graph_renderer.edge_renderer.data_source.data["colors"] = ["black"] * L
graph_renderer.edge_renderer.data_source.data["widths"] = [2] * L

plot.renderers.append(graph_renderer)


colors = Spectral10
widths = list(range(10))

def update():
    print('updating')
    graph_renderer.edge_renderer.data_source.data["colors"] = [random.choice(colors)]*L
    graph_renderer.edge_renderer.data_source.data["widths"] = [random.choice(widths)]*L
    graph_renderer.edge_renderer.data_source.data["start"] = [random.choice(graph_renderer.edge_renderer.data_source.data['end'])]*L
    graph_renderer.node_renderer.data_source.data["colors"] = [random.choice(colors)]*L

button = Button()
button.on_click(update)

layout = Column(button, plot)

doc = curdoc()
doc.add_root(layout)

show(layout)