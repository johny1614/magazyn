import matplotlib.pyplot as plt


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
    plt.title('Ilość pojazdów opuszczających układ - akcje wedle wyuczonej strategii')
    plt.savefig('images_generated/plot_cars_out.png')
    plt.close()
