# name tag problem

# https://oeis.org/A003111
# https://oeis.org/A006717

from itertools import permutations


def genCyclicPerms(perm):
    '''yields all cyclic perms (rotations to the right/left) for perm'''
    for i in range(len(perm)):
        yield perm[-i:]+perm[:-i]


def getNumOfMatches(perm):
    '''returns number of matches (element equals its index) for perm'''
    numOfMatches = 0
    for i in range(len(perm)):
        if i == perm[i]:
            numOfMatches += 1
    return numOfMatches


def getPermsWithOneMatch(n):
    '''returns list of perms of length n with only one match'''
    permsWithOneMatch = []
    for perm in permutations(range(1, n)):
        # fix first person to get unique perms (necklaces)
        perm = (0,) + perm
        for cyclicPerm in genCyclicPerms(perm):
            if getNumOfMatches(cyclicPerm) != 1:
                break
        else:
            permsWithOneMatch.append(perm)
    return permsWithOneMatch


def writeSolutionsToFile(fileName, solutions):
    with open(fileName+'.txt', 'w') as f:
        f.write('\n'.join([str(solution) for solution in solutions]))


def solveMPMP(n):
    solutions = getPermsWithOneMatch(n)
    print(f'There are {len(solutions)} unique perms of length {n} with one match:')
    print(*solutions, sep='\n')
    # writeSolutionsToFile('mpmp01', solutions)


# driver code
solveMPMP(7)
