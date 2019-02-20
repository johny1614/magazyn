import sys
sys.path.append("..")
from params.params import FlowParams
def q(p):
    q=p*(1-p/FlowParams.p_max)*FlowParams.v_max
    return q if q>0 else 0
def positive(p):
    return p if p>0 else 0
def gamma_wylot_(p):
    if(p<FlowParams.p_max/2):
        return q(p)
    return q(FlowParams.p_max/2)
def edgeColor(p_actual,p_min=0.0,p_max=FlowParams.p_max):
    # print("p_actual",p_actual)
    # print("pierwszy",255/(p_min-p_max)*p_actual)
    # print("drugi",-255*p_max/(p_min-p_max))
    actualGreen=255/(p_min-p_max)*p_actual-255*p_max/(p_min-p_max)
    actualRed=255/(p_max-p_min)*p_actual-255*p_min/(p_max-p_min)
    color="rgb("+str(actualRed)+","+str(actualGreen)+",0)"
    return color