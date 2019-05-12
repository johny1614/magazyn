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

    def saveToJson(self):
        dicSelf = attr.asdict(self)
        jsonData = json.dumps(dicSelf)
        with open('../../front/src/assets/densities/' + self.netName + '_' + self.densityName + '.json',
                  'w') as outfile:
            outfile.write(str(jsonData))
            outfile.close()
