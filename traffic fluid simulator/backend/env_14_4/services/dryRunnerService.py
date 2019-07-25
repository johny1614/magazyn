from copy import deepcopy


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def dry_run(env, actions, already_deep_copied=False):
    if not already_deep_copied:
        env_copy = env.deepCopy()
        env_copy.step(actions)
    else:
        env_copy = env
    rewards = [0, 0, 0]
    rewards = []
    for i in range(3):
        reward_i = sum([x[i] for x in env_copy.global_rewards[-4:]])
        rewards.append(reward_i)
    return env_copy, rewards


doggie = Dog('azor', 2)
doggie2 = deepcopy(doggie)
doggie2.age = 16
print(doggie.age)
