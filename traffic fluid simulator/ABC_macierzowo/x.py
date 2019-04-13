import json

data = {'values': [{
    'time': 0,
    'densities': [0, 0, 0, 0, 0, 0]},
    {
        'time': 1,
        'densities': [1, 1, 0, 0, 0, 0]},
    {
        'time': 2,
        'densities': [2, 2, 0, 0, 0, 0]},
    {
        'time': 3,
        'densities': [3, 3, 33, 0, 0, 0]}
]
}
with open('../front/src/assets/densities/net1_den1.json', 'w') as outfile:
    json.dump(data, outfile)
