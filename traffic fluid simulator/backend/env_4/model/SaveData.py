class SaveData:
    def __init__(self, learningEpochs, learningMethod):
        self.learningEpochs = learningEpochs
        self.learningMethod = learningMethod
        self.nets = []

    def add_net(self, globalState):  # globalState: GlobalState
        self.nets.append({'densities': tuple(globalState.x)})

    def attach_lights(self, lights):
        for i in range(len(lights)):
            self.nets[i - 1]['lights'] = hash_(lights[i])


def hash_(action):
    return tuple([tuple(a) for a in action])
