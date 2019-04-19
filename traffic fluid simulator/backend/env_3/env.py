import numpy as np
from matrix_3 import T,x0, A_WAITING ,UP_A_green,DOWN_A_green,u
#
# -A-B-
#      -E-F
# -c_D-
class Env:
    def __init__(self,x_size,epochs_number):
        self.waitFlag=False
        self.waitTime=0
        self.incoming_A=self.hash_(A_WAITING)
        self.static_switch_time=1
        self.A=self.hash_(UP_A_green)
        self.wating_A=None
        self.x=[0]*epochs_number
        self.x[0]=x0
        self.y=[0]*epochs_number
        self.t=0
        self.action_space=[UP_A_green,DOWN_A_green]
    def hash_(self,action):
        return tuple([tuple(a) for a in action])
    def do_action(self):
        # print('do action- A',self.A)
        t = self.t
        self.x[t]=np.dot(self.A,self.x[t-1])
        self.x[t][0]+=u[t-1][0]
        self.x[t][1]+=u[t-1][1]
        self.y[t]=self.x[t][-1]
        return self.x[t],self.y[t]
    def switch_wait(self,A):
        pass
    def step(self,A):
        self.t += 1
        #stay
        # print('A',A)
        # print('self.A',self.A)
        if(self.A==A):
            return self.do_action()
        # switch
        if(self.incoming_A == A):
            # we can use light
            if(self.waitTime == 0):
                self.A = self.incoming_A
                self.do_action()
        else: # we cannot use light yet so we wait
            self.waitTime -= 1
            self.A = self.hash_(A_WAITING)
            self.incoming_A=A
        return self.do_action()

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