import json

from typing import List

import attr

from model.Net import Net


@attr.s(auto_attribs=True)
class ExportData:
    learningMethod: str
    learningEpochs: int
    nets: List[Net]
    netName: str
    densityName: str

    def shift_lights(self):
        for i in range(len(self.nets))[:-1]:
            self.nets[i].lights = self.nets[i + 1].lights

    def saveToJson(self):
        self.shift_lights()
        dicSelf = attr.asdict(self)
        jsonData = json.dumps(dicSelf)
        with open('../../front/src/assets/densities/' + self.netName + '_' + self.densityName + '.json',
                  'w') as outfile:
            outfile.write(str(jsonData))
            outfile.close()


def shift(lista, n):
    return lista[n:] + lista[:n]
