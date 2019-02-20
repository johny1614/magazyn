class FlowParams:
    p_init=0.02
    v_max=33.0
    p_max=0.25
    q_start=1.2
    d_t=0.5
    d_x=20.0
    x_max=1000.0
    t_max=300.5
    q_init=None
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