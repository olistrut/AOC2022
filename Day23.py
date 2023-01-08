exec(open("aochelper.py").read())
import collections

def solve(filename, rounds = 10):
    result1 = 0
    result2 = 0

    file = open(filename)

    directions = ["N", "S", "W", "E"]
    currentDirIndex = 0

    # setup grid
    rows = file.read().split("\n")
    size = len(rows) + 1

    # set up only once es the grid only ever expands and never shrinks
    north = size + 1
    south = -1
    east = -1
    west = size + 1

    elvePos = {}

    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == "#":
                elvePos[(y,x)] = True

    i = 0
    nonMoving = 0
    while nonMoving != len(elvePos):
        nonMoving = 0
        proposals = collections.defaultdict(list)

        for e in elvePos.keys():
            # if nothing in surroundings, do nothing
            yStep = [-1, 0, 1]
            xStep = [-1, 0, 1]
            conflict = any (True for (yy, xx) in [(-1,-1), (-1,0), (-1,1), (+1,0), (1,1), (1,-1), (0,-1), (0,1)] if (e[0]+yy,e[1]+xx) in elvePos)

            propFound = False
            if conflict == False:
                # print("Elf ", num," at ",e[0], ",", e[1], "not moving")
                proposals[(e[0], e[1])].append((e[0],e[1]))
                propFound = True
                nonMoving += 1
            else:
                for attempt in range(len(directions)):
                    direction = directions[(currentDirIndex + attempt) % len(directions)]
                    if direction == "N":
                        stepCandidates = [(-1,0), (-1,1), (-1,-1)]
                    elif direction == "S":
                        stepCandidates = [(1,0), (1,1), (1,-1)]
                    elif direction == "W":
                        stepCandidates = [(-1, -1), (0, -1), (1, -1)]
                    elif direction == "E":
                        stepCandidates = [(-1, 1), (1, 1), (0, 1)]

                    conflict = any(True for (yy, xx) in stepCandidates if (e[0] + yy, e[1] + xx) in elvePos)

                    if conflict == False:
                        # found a candidate target position
                        propFound = True
                        if direction == "N":
                            proposals[(e[0] - 1, e[1])].append((e[0], e[1]))
                        elif direction == "S":
                            proposals[(e[0] + 1, e[1])].append((e[0], e[1]))
                        elif direction == "E":
                            proposals[(e[0], e[1] + 1)].append((e[0], e[1]))
                        elif direction == "W":
                            proposals[(e[0], e[1] - 1)].append((e[0], e[1]))
                        break

            # if no proposal found in any direction, we do not propose a new position.
            # no additional conflict risk as all other proposals already checked against current position

        for proposalCoordinates, proposalList in proposals.items():
            #p = list(proposals[k])
            if len(proposalList) == 1:
                del elvePos[proposalList[0]]
                elvePos[proposalCoordinates] = True

        if (i == rounds):
            for e in elvePos.keys():
                y = e[0]
                x = e[1]
                south = max(south, y)
                east = max(east, x)
                north = min(north, y)
                west = min(west, x)

            result1 = (south-north+1) * (east-west+1) - len(elvePos)

        # next round
        currentDirIndex = (currentDirIndex + 1) % len(directions)

        #if i % 25 == 0:
        #    print("Non moving: ", nonMoving, " of ", len(elvePos), " elves in round ", i)
        i += 1

    result2 = i
    return result1, result2


########################
aocrunonce(23, True, True)

