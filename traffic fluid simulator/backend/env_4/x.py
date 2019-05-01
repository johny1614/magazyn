from env_data import start_A, get_Agents
from env import Env
from jsonSaver import saveToJson
time = 10
env = Env(time)
save_data = {
    "learningEpochs": 0,
    "learningMethod": "Random",
    "nets": []}
for x in range(time - 1):
    actions = [agent.getRandomAction() for agent in env.agents]
    state, y = env.step(actions)
    save_data["nets"].append({'lights':state.x,'lights':state.lights})
    print(state.x)
    saveToJson('net_4', 'random', save_data)
    # data = {
    #     'nets': nets,
    #     'rewards sum': reward_sum,
    #     'gamma': gamma,
    #     'learningEpochs': len(epochs),
    #     'learningMethod': 'Monte Carlo',
    #     # 'turns':env.turns
    # }
