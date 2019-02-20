from params import Params
def q(p):
    q=p*(1-p/Params.p_max)*Params.v_max
    return q if q>0 else 0
def positive(p):
    return p if p>0 else 0
def gamma_wylot_(p):
    if(p<Params.p_max/2):
        return q(p)
    return q(Params.p_max/2)
