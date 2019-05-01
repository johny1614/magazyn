from env_data import start_A

class SaveData:
    def __init__(self,learningEpochs,learningMethod):
        self.learningEpochs=learningEpochs
        self.learningMethod = learningMethod
        self.nets=[]
    def add_net(self,globalState): # globalState: GlobalState
        self.nets.append({'lights':hash_(globalState.A),'densities':tuple(globalState.x)})

def hash_(action):
    return tuple([tuple(a) for a in action])