from nn_trainer import get_batches
from services.agentFactory import get_LearnSmartAgents
import matplotlib.pyplot as plt

def draw_batches_from_agent(agents,file_name='batches_greedy.png'):
    a=23
    fig, ax = plt.subplots()
    states_occured=[mem.state.to_learn_array(agents[0])[0] for mem in agents[0].memories]
    print('states',len(states_occured))
    for i in range(len(states_occured[0])):
        dens_i=[x[i] for x in states_occured]
        x_coordinate_for_i = [i] * len(dens_i)
        ax.plot(x_coordinate_for_i, dens_i, 'o', color=(0, 0, 0))
    fig.savefig(file_name)



def draw_batches(file_name='batches.png'):
    agents = get_LearnSmartAgents()
    batches = get_batches(agents)
    x_batch=batches[0]['x_batch']
    y_batch=batches[0]['y_batch']
    fig, ax = plt.subplots()
    for i in range(len(x_batch[0])):
        dens_i=[x[i] for x in x_batch]
        x_coordinate_for_i = [i] * len(dens_i)
        ax.plot(x_coordinate_for_i, dens_i, 'o', color=(0, 0, 0))
    fig.savefig(file_name)

def draw_colored_batches(agents,file_name='batches.png'):
    fig, ax = plt.subplots()
    # na razie dla pierwszego density
    i=0
    actions_0=[mem.state.to_learn_array(agents[0])[i] for mem in agents[0].memories if mem.action==0]
    actions_1=[mem.state.to_learn_array(agents[0])[i] for mem in agents[0].memories if mem.action==1]
    actions_2=[mem.state.to_learn_array(agents[0])[i] for mem in agents[0].memories if mem.action==2]
    actions_orange=[mem.state.to_learn_array(agents[0])[i] for mem in agents[0].memories if mem.action=='orange']
    ax.plot([0]*len(actions_0),actions_0, 'o', color=(1, 0, 0))
    ax.plot([0]*len(actions_1),actions_1, 'o', color=(0, 1, 0))
    ax.plot([0]*len(actions_2),actions_2, 'o', color=(0, 0, 1),marker_size=10)
    ax.plot([0]*len(actions_orange),actions_orange, 'o', color=(0, 0, 0))



    # agents = get_LearnSmartAgents()
    # batches = get_batches(agents)
    # x_batch=batches[0]['x_batch']
    # y_batch=batches[0]['y_batch']
    # for i in range(len(x_batch[0])):
    #     dens_i=[x[i] for x in x_batch]
    #     x_coordinate_for_i = [i] * len(dens_i)
    fig.savefig(file_name)
    a=2

if __name__ == "__main__":
    # while True:
    draw_batches()
