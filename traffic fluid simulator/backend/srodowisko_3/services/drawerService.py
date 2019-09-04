from services.globals import Globals
from matplotlib import pyplot as plt

def draw_rewards_mean(results,run=Globals().run_no):
    plt.plot([res[0] for res in results])
    plt.title('Średnia wszystkich nagród - akcje wedle wyuczonej strategii')
    plt.savefig('images_generated/plot_rewards_mean' + str(run) + '.png')
    plt.close()


def draw_cars_out(results,run=Globals().run_no):
    plt.plot([res[2] for res in results])
    plt.title('Ilość pojazdów opuszczających układ - akcje wedle wyuczonej strategii')
    plt.savefig('images_generated/plot_cars_out' + str(run) + '.png')
    plt.close()

