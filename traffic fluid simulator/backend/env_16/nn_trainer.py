import random
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential

from services.agentFactory import get_LearnSmartAgents, get_SmartAgents
from services.globals import Globals


def get_batches(agents):
    batches = []
    for i in range(len(agents)):
        filename = 'static_files/x_batch_agent_' + str(i) + '.txt'
        x_batch = np.array(np.loadtxt(filename, delimiter=','))
        filename = 'static_files/y_batch_agent_' + str(i) + '.txt'
        y_batch = np.array(np.loadtxt(filename, delimiter=','))
        batches.append({'x_batch': x_batch, 'y_batch': y_batch})
    return batches


def create_model(layers, activation, l_rate):
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=7, activation='linear'))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(2))  # Note: no activation beyond this point
    model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
    return model


def train(learntAgents=True, max_time_learn=60, agents=None,shuffle=True,batches=None):
    if agents is None:
        if not learntAgents:
            agents = get_SmartAgents()
        else:
            agents = get_LearnSmartAgents()
    if batches is None:
        batches = get_batches(agents)
    models = [agent.model for agent in agents]
    for i in range(len(agents)):
        start_time = timer()
        x_batch = batches[i]['x_batch']
        y_batch = batches[i]['y_batch']
        model = models[i]
        weights_best = model.get_weights()
        val_loss = 10 ** 10
        val_loss_best = 10 ** 10
        escape_flag = False
        escape_val = 0
        inne = 0
        te_same = 0
        start_flag=True
        while timer() - start_time < max_time_learn and not escape_flag:
            # print('na start mamy res.history[val_loss]',model.history['val_loss'][-1])
            # if shuffle:
            #     validation_indexes = random.sample(range(len(x_batch)),int(len(x_batch)/10))
            #     validation_x,validation_y = [[x_batch[index_x] for index_x in validation_indexes]],[[y_batch[index_y] for index_y in validation_indexes]]
            #     res = model.fit(x_batch, y_batch, batch_size=Globals().vp().batch_size,
            #                     initial_epoch=Globals().epochs_done,
            #                     epochs=Globals().epochs_done + Globals().epochs_learn,
            #                     validation_data=(validation_x,validation_y),
            #                     verbose=0)  # callbacks=[Globals().tensorboard,agents[i].weights_history_callback]
            wagi_przed_uczeniem = model.get_weights()
            res = model.fit(x_batch, y_batch, batch_size=Globals().vp().batch_size,
                            initial_epoch=Globals().epochs_learn_done,
                            epochs=Globals().epochs_learn_done + Globals().vp().epochs_learn,
                            validation_split=0.2,
                            verbose=0)  # callbacks=[Globals().tensorboard,agents[i].weights_history_callback]
            same = True
            porownanie = wagi_przed_uczeniem [0] == model.get_weights()[0]
            for porownanie_warstwa in porownanie:
                if any([s == False for s in porownanie_warstwa]):
                    same = False
            if same:
                te_same += 1
                print(f'wagi te same {te_same} inne {inne}')
            else:
                inne += 1
            # print('wagi te same - uczenie', same)
            Globals().epochs_learn_done += Globals().vp().epochs_learn
            if start_flag:
                # print('res history z start_flag to',res.history['val_loss'])
                start_flag=False
            if res.history['val_loss'][-1] < val_loss_best:
                res_hist=res.history['val_loss'][-1]
                # print(f'res.history {res_hist} lepsze niz {val_loss_best}')
                val_loss_best = res.history['val_loss'][-1]
                weights_best = model.get_weights()
            if res.history['val_loss'][-1] >= val_loss:
                escape_val += 1
                # print('escape_val',escape_val)
                # print('val loss',res.history['val_loss'][-1])
                if escape_val > 10:
                    escape_flag = True
                #     print('przerwalbym!!!!!!')
                # print('wynik sieci', res.history['val_loss'][-1])
                val_loss = 10 ** 10
            else:
                val_loss = res.history['val_loss'][-1]
            if not (timer() - start_time < max_time_learn and not escape_flag):
                print('loss',res.history['val_loss'][-1])
        Globals().last_weights == model.get_weights()
        model.set_weights(weights_best)
        # print('wagi po', model.get_weights())
        # print('porownanko',model.get_weights()[0])
        # print('wagi takie same',wagi_przed[0]==model.get_weights()[0])
        model.save('static_files/model-agent' + str(i) + '.h5')


def plot_pred_memory(name=str(Globals().run_no)):
    plt.plot([pred[0][0] for pred in Globals().pred_plot_memory], color='red', label='0')
    plt.plot([pred[0][1] for pred in Globals().pred_plot_memory], color='green', label='1')
    plt.legend()
    plt.title('Nagrody przewidziane dla akcji podjętych podczas monitorowanego stanu')
    plt.savefig('plot' + name + '.png')
    plt.close()


if __name__ == "__main__":
    train()
