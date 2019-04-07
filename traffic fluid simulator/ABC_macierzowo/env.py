import numpy as np
from matrix import T,x0,A_a_green,A_b_green,u
# -A-
#     -C-
# -B-
class Env:
    def __init__(self,n):
        self.n=n
        self.x=[0]*(n+1)
        self.x[0]=x0
        self.y=[0]*(n+1)
        self.t=0
        self.action_space=[A_a_green,A_b_green]
    def step(self,A):
        self.t+=1
        t=self.t
        self.x[t]=np.dot(A,self.x[t-1])
        self.x[t][0]+=u[t-1][0]
        self.x[t][1]+=u[t-1][1]
        # print('x-'+str(t),self.x[t])
        self.y[t]=self.x[t][2]
        # print('y-'+str(t),self.y[t])
        return self.x[t],self.y[t]
    def dry_step(self,A):
        t=self.t
        t=t+1
        x_t=np.dot(A,self.x[t-1])
        print('x-'+str(t),x_t)
        x_t[0]+=u[t-1][0]
        x_t[1]+=u[t-1][1]
        y_t=x_t[2]
        # print('y-'+str(t),self.y[t])
        return x_t,y_t