import numpy as np
from matrices import T,x0, A_ORANGE ,UP_A_green,DOWN_A_green,u
#
# -A-B-
#      -E-F
# -c_D-
# road_1
#           road_3
# road_2

class Env:
    def __init__(self, max_time):
        self.x_size=6
        self.min_light_duration = 3
        self.orange_light_duration = 1
        self.A=self.getActionMatrix('road_1')
        self.incoming_A = None
        self.actual_light_duration=0
        self.x= [self.x_size*[0]] * max_time
        self.x[0]=x0
        self.y= [0] * max_time
        self.t=0
    def getActionSpace(self):
        if(self.actual_light_duration>self.min_light_duration):
            return ['road_1','road_2']
        else:
            return ['wait']
    def getActionName(self,actionMatrix):
        if(actionMatrix==A_ORANGE):
            light = "green" if self.actual_light_duration>self.orange_light_duration else "orange"
            return "wait_"+self.getActionName(self.A)+"_"+light
        elif (actionMatrix == UP_A_green):
            return "road_1"
        elif(actionMatrix==DOWN_A_green):
            return "road_2"
        return "action-name-error"
    def getActionMatrix(self,actionName):
        if(actionName=="road_1"):
            return self.hash_(UP_A_green)
        elif(actionName=="road_2"):
            return self.hash_(DOWN_A_green)
        elif(actionName=="wait"):
            if(self.actual_light_duration>self.min_light_duration):
                return self.A
            else:
                return A_ORANGE
    def hash_(self,action):
        return tuple([tuple(a) for a in action])
    def do_action(self,A):
        t = self.t
        self.x[t]=np.dot(A,self.x[t-1])
        self.x[t][0]+=u[t-1][0]
        self.x[t][2]+=u[t-1][1]
        self.y[t]=self.x[t][-2]
        actionName=self.getActionName(A)
        return self.x[t],self.y[t],actionName
    def switch_wait(self,A):
        pass
    def step(self,actionName):
        self.t += 1
        A=self.getActionMatrix(actionName)
        if(actionName=='wait' and self.actual_light_duration<self.orange_light_duration):
            self.actual_light_duration+=1
            return self.do_action(A_ORANGE)
        elif(A!=self.A and not actionName=='wait'):
            self.A=A
            self.actual_light_duration=0
            return self.do_action(A_ORANGE)
        elif(A==self.A or actionName=='wait'):
            self.actual_light_duration+=1
            return self.do_action(self.A)
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