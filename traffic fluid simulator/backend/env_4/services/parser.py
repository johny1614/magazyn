def get_G(rewards, gamma):
    G = [0] * len(rewards)
    G_value = rewards[-1]
    G[len(rewards) - 1] = G_value
    for i in reversed(range(len(rewards) - 1)):
        G_value = gamma * G_value + rewards[i]
        G[i]=G_value
    return G
