from light_service import LightService
class Epoch:
    def __init__(self,networks,name):
        self.networks=networks
        self.light_service = LightService(self)
        self.name=name
    def rate(self):
        all_q=[]
        networkRoads = [network.roads for network in self.networks]
        for roads in networkRoads:
            roads_cells=[road.normalGrid.cells for road in roads]
            for cells in roads_cells:
                for cell in cells:
                    all_q.append(cell.q)
        self._rate=sum(all_q)
        print(self._rate)
