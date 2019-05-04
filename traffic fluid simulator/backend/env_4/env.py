import numpy as np
from env_data import x0, u, start_A, get_Agents, curve_densities, stayCoordinates


# trojkatne - 3 skrzyzowania, razem 6 drog

class GlobalState:
    def __init__(self,x,agents,A):
        self.x=x
        self.lights=[(agent.actual_phase,agent.min_phase_duration) for agent in agents]
        self.A=A
class Env:
    def __init__(self, max_time):
        self.max_time=max_time
        self.x_size=36
        self.A=start_A()
        self.agents=get_Agents()
        self.x= [self.x_size*[0]] * max_time
        self.x[0]=x0
        self.y=[0] * max_time
        self.A_storage=[0]*(max_time-1)
        self.t=0
    def modify_A(self):
        for agent in self.agents:
            self.A=agent.modify_A(self.A)
    def do_action(self):
        t = self.t
        self.A=start_A()
        self.modify_A()
        self.A_storage[t-1]=self.A
        self.x[t]=np.dot(self.A,self.x[t-1])
        self.x[t][0]+=u[t-1][0]
        self.x[t][3]+=u[t-1][1]
        self.x[t][6]+=u[t-1][1]
        self.y[t]=self.x[t][29]+self.x[t][35]+self.x[t][32]
        globalState=GlobalState(self.x[t],self.agents,self.A)
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
        return x_t,y_t
    def get_global_action_space(self):
        global_action_space=[]
        for agent in self.agents:
            localSpace=agent.getLocalActionSpace()
            global_action_space.append(localSpace)
        return global_action_space
    def pretty_print(self):
        for t in range(self.max_time):
            print('time:'+str(t))
            print('density',self.x[t])
            print('density[9]',self.x[t][9])
            print('A > 0 na:')

    def pretty_print_A(self,t):
        print('A',t)
        for row_index in range(len(self.A_storage[t])):
            row = self.A_storage[t][row_index]
            for column_index in range(len(row)):
                cell = row[column_index]
                if (cell > 0 and row_index != column_index + 1):
                    print('wartosc ' + str(cell) + ' na:', (row_index, column_index))
    def pretty_print_4(self):
        t=4
        print('densities 3',self.x[t-1])
        self.pretty_print_A(4)
        print('densities 4',self.x[t])