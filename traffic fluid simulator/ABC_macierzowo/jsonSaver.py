import json
def saveToJson(netName,densityName,data):
    with open('../front/src/assets/densities/'+netName+'_'+densityName+'_python.json', 'w') as outfile:
        json.dump(data, outfile)
