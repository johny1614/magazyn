class TurnTable:
 # droga wylotowa, droga wlotowa z naprzeciwka, droga wlotowa ze skretu w prawo
    input_flow = [
        [4, 2, 1],
        [5, 3, 2],
        [6, 0, 3],
        [7, 1, 0]
    ]
    # droga,prawdopodobienstwo jazdy prosto, prawdopodobienstwo jazdy w prawo
    turn_probability =[
        [0, 0.3, 0.7],
        [1, 0.3, 0.7],
        [2, 0.3, 0.7],
        [3, 0.3, 0.7],
        [4, 0.3, 0.7],
        [5, 0.3, 0.7],
        [6, 0.3, 0.7],
        [7, 0.3, 0.7]
    ]
    # # droga wlotowa, droga wylotowa, prawdopodobienstwo
    flow_probability =[
        [0, 4, 0],
        [0, 5, 0],
        [0, 6, 0.1],
        [0, 7, 0.9],

        [1, 4, 0.1],
        [1, 5, 0],
        [1, 6, 0],
        [1, 7, 0.9],

        [2, 4, 0.7],
        [2, 5, 0.3],
        [2, 6, 0],
        [2, 7, 0],

        [3, 4, 0],
        [3, 5, 0.3],
        [3, 6, 0.3],
        [3, 7, 0]
    ]
    
