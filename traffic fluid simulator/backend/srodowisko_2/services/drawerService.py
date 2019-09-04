import matplotlib.pyplot as plt

from services.globals import Globals


def draw_cars_out(results,no):
    plt.plot([res[2] for res in results])
    plt.title('Ilość pojazdów opuszczających układ - akcje wedle wyuczonej strategii')
    plt.savefig('images_generated/plot_cars_out' + str(no) + '.png')
    plt.close()


def plot_pred_memory(no):
    plt.plot([pred[0][0] for pred in Globals().pred_plot_memory], color='red', label='0')
    plt.plot([pred[0][1] for pred in Globals().pred_plot_memory], color='green', label='1')
    plt.legend()
    plt.title('Nagrody przewidziane dla akcji podjętych podczas monitorowanego stanu')
    plt.savefig('images_generated/rewards_' + no + '.png')
    plt.close()
