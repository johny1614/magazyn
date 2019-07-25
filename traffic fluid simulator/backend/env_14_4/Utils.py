def nested_sum(L):
    total = 0  # don't use `sum` as a variable name
    for i in L:
        if isinstance(i, list):  # checks if `i` is a list
            total += nested_sum(i)
        else:
            total += i
    return total
def empty_3_list():
    return [[], [], []]

def count_rewards(env):
    memsum = 0
    i = 0
    for agent in env.agents:
        for mem in agent.memories:
            i += 1
            memsum += mem.reward
    return memsum, memsum / i

def empty_dic():
    return {}
