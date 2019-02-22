class FlowParams:
    p_init=0.00
    p_max=0.25
    p_1_source=0.2
    p_2_source=0.1
    d_t=1
    d_x=50.0
    x_max=500.0
    t_max=40
    q_init=None
    _lambda=2
class BokehParams:
    x_range=(-2,2002)
    y_range=(-6,6)
    point_height=0.2
    point_width=0.2
    class Slider:
        start=0.0
        end=FlowParams.t_max
    class Edge:
        minWidth=2.0
        maxWidth=12.0