import matplotlib.pyplot as plt

from services.globals import Globals


def draw_rewards_mean(results):
    plt.plot([res[0] for res in results])
    plt.title('Średnia wszystkich nagród - akcje wedle wyuczonej strategii')
    plt.savefig('images_generated/plot_rewards_mean.png')
    plt.close()


def draw_rewards(results):
    plt.plot([res[1] for res in results])
    plt.title('Suma nagród - akcje wedle wyuczonej strategii')
    plt.savefig('images_generated/plot_rewards.png')
    plt.close()


def draw_cars_out(results):
    plt.plot([res[2] for res in results])
    plt.title('Liczba pojazdów opuszczających układ')
    plt.savefig('images_generated/plot_cars_out.png')
    plt.close()


def draw_cars_out_percentage(results):
    plt.plot([res[5] for res in results])
    plt.title('Procent pojazdów opuszczających układ')
    plt.savefig('images_generated/plot_cars_out_percentage.png')
    plt.close()


def draw_max(results):
    plt.plot([res[4] for res in results])
    plt.title('Liczba pojazdów napływających do układu')
    plt.savefig('images_generated/plot_cars_in.png')
    plt.close()


def plot_losses():
    losses = Globals().loss_history
    plt.plot([loss for loss in losses[0]],label='Agent 0')
    plt.plot([loss for loss in losses[1]],label='Agent 1')
    plt.plot([loss for loss in losses[2]],label='Agent 2')
    plt.plot([loss for loss in losses[3]],label='Agent 3')
    plt.legend()
    plt.title('Wartości straty')
    plt.savefig('images_generated/losses.png')
    plt.close()

