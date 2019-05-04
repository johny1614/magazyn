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


def getGroup(density):
    for i in range(len(groups)):
        if density >= groups[i][0] and density >= groups[i][1]:
            return i
    return len(groups)


def getRange(groupNumber):
    return {"from": groups[groupNumber][0], "to": groups[groupNumber][1]}
