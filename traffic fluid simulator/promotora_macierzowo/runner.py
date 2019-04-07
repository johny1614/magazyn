import numpy as np
from matrix import T,x0,A_niepar,A_par,u
                  # A->B       ->G->H
# siec drog to:         ->E->F
                  # C->D       ->I->J
n=11
x=[0]*(n+1)
x[0]=x0
print('x-0',x[0])
for t in range(1,n):
    if(t%2==1):
        A=A_niepar
    else:
        A=A_par
    x[t]=np.dot(A,x[t-1])
    x[t][0]=u[t-1][0]
    x[t][2]=u[t-1][1]
