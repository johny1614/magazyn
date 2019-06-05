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

        print('done')

    # def shift_lights(self):
    #     for i in range(len(self.nets))[:-1]:
    #         self.nets[i].lights = self.nets[i + 1].lights

    def saveToJson(self):
        # self.shift_lights()
        dicSelf = attr.asdict(self)
        jsonData = json.dumps(dicSelf)
        with open('../../front/src/assets/densities/' + self.netName + '_' + self.densityName + '.json',
                  'w') as outfile:
            outfile.write(str(jsonData))
            outfile.close()


def shift(lista, n):
    return lista[n:] + lista[:n]
