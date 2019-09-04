from Env import Env
from model import SmartAgent
from model.ExportData import ExportData
from services.dryRunnerService import dry_run
from typing import List
from services.agentFactory import get_SmartAgents
from services.globals import Globals

orange = 'orange'
agents = get_SmartAgents()
env = Env(agents)
for agent in agents:
    agent.orange_phase_duration = 0
max_time = 36
Globals().time = 0
for t in range(max_time):
    actions = [0, 0, 0, 0]
    if t == 1:
        actions = [1, 1, 1, 1]
    if t == 2:
        actions = [2, 2, 2, 2]
    if t == 3:
        actions = [3, 3, 3, 3]
    if t > 10:
        for agent in agents:
            agent.orange_phase_duration = 2
    if t == 12:
        actions = [1, 1, 1, 1]

    env.step(actions)
    # self.x[self.t] = [i for i in range(40)] # w envie dodac!

for agent in agents:
    agent.reshape_rewards()

    exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                            netName='politechnika',
                            densityName='base_from_backend')
    exportData.saveToJson()
    a = 2
