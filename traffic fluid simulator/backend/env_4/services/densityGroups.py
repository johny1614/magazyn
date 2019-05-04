groups = [
    [0, 0],
    [1, 1],
    [2, 3],
    [3, 5],
    [6, 10],
    [11, 20],
    [21, 40],
    [41, 70],
    [71, 100],
    [101, 200],
]

def getGroup(number):
    for i in range(len(groups)):
        if(number>=groups[i][0] and number>=groups[i][1]):
            return i
    return len(groups)