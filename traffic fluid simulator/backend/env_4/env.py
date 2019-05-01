import numpy as np
from env_data import T,x0, A_ORANGE ,UP_A_green,DOWN_A_green,u,start_A,get_Agents

# trojkatne - 3 skrzyzowania, razem 6 drog

class GlobalState:
    def __init__(self,x,agents):
        self.x=x
        self.lights=[(agent.actual_phase,agent.min_phase_duration) for agent in agents]
class Env:
    def __init__(self, max_time):
        self.x_size=36
        self.A=start_A()
        self.agents=get_Agents()
        for agent in self.agents:
            agent.modify_A(self.A)
        self.x= [self.x_size*[0]] * max_time
        self.x[0]=x0
        self.y=[0] * max_time
        self.t=0
    def modify_A(self):
        for agent in self.agents:
            agent.modify_A(self.A)
    def do_action(self):
        t = self.t
        self.modify_A()
        self.x[t]=np.dot(self.A,self.x[t-1])
        self.x[t][0]+=u[t-1][0]
        self.x[t][3]+=u[t-1][1]
        self.x[t][6]+=u[t-1][1]
        self.y[t]=self.x[t][29]+self.x[t][35]+self.x[t][32]
        globalState=GlobalState(self.x,self.agents)
        return globalState,self.y[t]
    def switch_wait(self,A):
        pass
    def step(self,actions):
        self.t += 1
        for i in range(self.agents.__len__()):
            agent=self.agents[i]
            agent.pass_action(actions[i])
        self.modify_A()
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
    def get_global_action_space(self):
        print('e')