def count_rewards(env):
    memsum = 0
    i = 0
    for agent in env.agents:
        for mem in agent.memories:
            i += 1
            memsum += mem.reward
    return memsum, memsum / i
