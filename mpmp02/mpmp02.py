# classic jeep problem


def minFuel(d, c):
    '''returns minimum amount of fuel required to travel distance d
    by a vehicle with fuel tank capacity c; assumes d, c > 0'''
    x, n = 0, 0  # interval end, interval numeral
    dn = d/c  # normalized travel distance
    # move interval end until it exceeds distance
    while x + 1/(2*n+1) < dn:
        x += 1/(2*n+1)  # move interval end
        n += 1  # go to the next interval
    # linear function passing through point (xp,yp):
    # f(x) = a*x+b = a*x+(yp-a*xp) = a*(x-xp)+yp
    # in this interval: a = (2*n+1) and (xp,yp) = (x,n)
    return c*((2*n+1)*(dn-x)+n)


def createStepsRegardingFuel(fuel, n, v):
    '''creates list of steps as (action, value) regarding fuel (take/leave
    value amount of fuel) by modifing list of steps from previous interval'''
    # fuel = f[:]
    fuel.insert(0, ('take fuel', (2*n+1)*v))
    if n > 0:
        fuel.insert(1, ('leave fuel', (2*n-1)*v))
        fuel.insert(3, ('take fuel', v))
        for i in range(n-1):
            fuel.insert((i+2)*(i+3)-1, ('take fuel', v))
            fuel.insert((i+2)*(i+3)+1, ('take fuel', v))
    # return fuel


def createStepsRegardingMoves(moves, n, v):
    '''creates list of steps as (action, value) regarding moves (go forth/
    back value distance) by modifing list of steps from previous interval'''
    # moves = m[:]
    moves.insert(0, ('go forth', v))
    for i in range(n):
        moves.insert((i+1)*(i+2)-1, ('go back', v))
        moves.insert((i+1)*(i+2), ('go forth', v))
    # return moves


def travellingStrategy(d, c):
    '''returns optimal strategy (list of steps) to travel distance d
    by a vehicle with fuel tank capacity c with minimum amount of fuel'''
    x, n = 0, 0  # interval end, interval numeral
    dn = d/c  # normalized travel distance
    fuel = []  # list of steps regarding fuel
    moves = []  # list of steps regarding moves
    # move interval end until it exceeds distance
    while x + 1/(2*n+1) < dn:
        createStepsRegardingFuel(fuel, n, c/(2*n+1))
        createStepsRegardingMoves(moves, n, c/(2*n+1))
        x += 1/(2*n+1)  # move interval end
        n += 1  # go to the next interval
    else:
        createStepsRegardingFuel(fuel, n, c*(dn-x))
        createStepsRegardingMoves(moves, n, c*(dn-x))
    # strategy consists of alternating steps regarding fuel and moves
    return [pair for pairs in zip(fuel, moves) for pair in pairs]


def simulateTravel(strategy, minFuel):
    x, f = 0, 0  # current position, current fuel level
    n, stations = 0, [minFuel]  # interval numeral, fuel distribiution
    print(f'x = {x:.2f} | f = {f:.2f} | stations: ', end='')
    print(', '.join([f'{station:.2f}' for station in stations]))
    for action, value in strategy:
        if action == 'take fuel':
            f += value  # increase current fuel level
            stations[n] -= value  # decrease amount of fuel in station n
        elif action == 'leave fuel':
            f -= value  # decrease current fuel level
            stations.append(value)  # create new station with fuel
        elif action == 'go forth':
            f -= value  # fuel consumption
            x += value  # move forward to
            n += 1      # the next station
        elif action == 'go back':
            f -= value  # fuel consumption
            x -= value  # move backward to
            n -= 1      # the previous station
        print(f'x = {x:.2f} | f = {f:.2f} | stations: ', end='')
        print(', '.join([f'{station:.2f}' for station in stations]))


def writeSolutionToFile(fileName, strategy):
    with open(fileName+'.txt', 'w') as f:
        f.write('\n'.join([f'({a}, {v:.2f})' for a, v in strategy]))


def solveMPMP(d, c):
    print(f'minFuel({d}, {c}) = {minFuel(d,c):.2f}')
    strategy = travellingStrategy(d, c)
    # print('\n'.join([f'({a}, {v:.2f})' for a, v in strategy]))
    simulateTravel(strategy, minFuel(d, c))
    # writeSolutionToFile('mpmp02', strategy)


# driver code
solveMPMP(800, 500)
