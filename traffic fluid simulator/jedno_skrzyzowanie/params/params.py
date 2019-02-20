class FlowParams:
    p_init = 0.02
    v_max = 33.0
    p_max = 0.25
    q_start = 1.2
    d_t = 0.5
    d_x = 20.0
    x_max = 1000.0
    t_max = 300.5
    q_init = None
class BokehParams:
    x_start = -650
    x_end = 650
    y_start = -650
    y_end = 650
    point_height = 0.2
    point_width = 0.03
    plot_height=800
    plot_width=800
    class Slider:
        start = 0.0
        end = FlowParams.t_max
    class Edge:
        minWidth = 2.0
        maxWidth = 12.0
