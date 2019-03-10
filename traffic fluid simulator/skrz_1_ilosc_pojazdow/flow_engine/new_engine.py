import numpy as np
from matrices import M,P,O,move

def get_S(k):
    SZero=np.matrix(np.zeros((P[k].shape)))
    SkZero=M[k]*P[k][:,-1]
    SZero[:,0]=SkZero
    return SZero

S=get_S(0)
W=P[0][:,-1]-S
P1=P[0]*move+O[0]+W+S
#
print(P1)