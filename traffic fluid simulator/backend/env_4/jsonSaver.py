import json
def saveToJson(netName,densityName,data):
    formatedData = json.dumps(data.__dict__,indent=4)
    with open('../../front/src/assets/densities/'+netName+'_'+densityName+'.json', 'w') as outfile:
        outfile.write(str(formatedData))
        outfile.close()
