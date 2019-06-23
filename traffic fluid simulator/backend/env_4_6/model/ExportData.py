import json
from typing import List
import attr
from numpy.core.multiarray import ndarray
from model.Net import Net

@attr.s(auto_attribs=True)
class ExportData:
    learningMethod: str
    learningEpochs: int
    nets: List[Net]
    netName: str
    densityName: str

    def __attrs_post_init__(self):
        for net_index in range(len(self.nets)):
            if isinstance(self.nets[net_index].densities, ndarray):
                self.nets[net_index].densities = self.nets[net_index].densities.tolist()
            if isinstance(self.nets[net_index].lights, ndarray):
                self.nets[net_index].lights = self.nets[net_index].lights.tolist()

    def saveToJson(self):
        # self.shift_lights()
        dicSelf = attr.asdict(self)
        try:
            jsonData = json.dumps(dicSelf)
            outfile = open('../../front/src/assets/densities/' + self.netName + '_' + self.densityName + '.json', 'w')
        except:
            outfile = open('../../../front/src/assets/densities/' + self.netName + '_' + self.densityName + '.json',
                           'w')
        outfile.write(str(jsonData))
        outfile.close()


def shift(lista, n):
    return lista[n:] + lista[:n]
