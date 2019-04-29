import json
def saveToJson(netName,densityName,data):
    with open('../front/src/assets/densities/'+netName+'_'+densityName+'.json', 'w') as outfile:
        # formatedData = json.loads(data)
        json.dump(data, outfile, indent=4)
        outfile.close()
