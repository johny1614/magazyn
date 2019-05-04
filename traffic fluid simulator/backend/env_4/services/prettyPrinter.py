def pretty_print(env):
    for t in range(env.max_time):
        print('time:' + str(t))
        print('density', env.x[t])
        print('density[9]', env.x[t][9])
        print('A > 0 na:')


def pretty_print_A(env, t):
    print('A', t)
    for row_index in range(len(env.A_storage[t])):
        row = env.A_storage[t][row_index]
        for column_index in range(len(row)):
            cell = row[column_index]
            if cell > 0 and row_index != column_index + 1:
                print('wartosc ' + str(cell) + ' na:', (row_index, column_index))


def pretty_print_4(env):
    t = 4
    print('densities 3', env.x[t - 1])
    env.pretty_print_A(4)
    print('densities 4', env.x[t])
