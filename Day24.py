exec(open("aochelper.py").read())
import math

class Blizzard:
    def __init__(self, direction, x, y):
        self.direction = direction
        self.x = x
        self.y = y

def calcBlizzards(blizzards, width, height):
    tmpBlizzards = blizzards.copy()

    mapCache = [[]]

    maxRounds = math.lcm((width - 2), (height - 2))

    for round in range(maxRounds):
        tmpSpace = [["." for i in range(width)] for j in range(height)]
        for xx in range(width):
            tmpSpace[0][xx] = "#"
            tmpSpace[height - 1][xx] = "#"
        for yy in range(height):
            tmpSpace[yy][0] = "#"
            tmpSpace[yy][width - 1] = "#"
        tmpSpace[0][1] = "."
        tmpSpace[height - 1][width - 2] = "."

        for b in tmpBlizzards:
            if b.direction == ">":
                if b.x + 1 < width - 1:
                    b.x += 1
                else:
                    b.x = 1
            elif b.direction == "<":
                if b.x - 1 > 0:
                    b.x -= 1
                else:
                    b.x = width - 2
            elif b.direction == "^":
                if b.y - 1 > 0:
                    b.y -= 1
                else:
                    b.y = height - 2
            elif b.direction == "v":
                if b.y + 1 < height - 1:
                    b.y += 1
                else:
                    b.y = 1
            tmpSpace[b.y][b.x] = "B"

        mapCache.append(tmpSpace)

    return mapCache


def bfs(x, y, width, height, blizzards):
    clock = 0
    stateQueue = [(clock, x, y)]

    mapCache = calcBlizzards(blizzards, width, height)

    step = 1

    targetX = width - 2
    targetY = height - 1

    visited = {}

    while stateQueue:
        clock, x, y = stateQueue.pop(0)

        if (x == targetX) and (y == targetY):
            # print("Found exit at ", x, y, " at time ", clock)
            stateQueue = []
            visited = {}

            if step == 1:
                result1 = clock
                # print(" Going back to entry...")
                targetX = 1
                targetY = 0
                stateQueue.append((clock + 1, x, y))
            elif step == 2:
                # print("  Marching towards the exit again...")
                targetX = width - 2
                targetY = height - 1
                stateQueue.append((clock + 1, x, y))
            elif step == 3:
                result2 = clock
                return result1, result2

            step += 1
        clock += 1

        tmpSpace = mapCache[((clock - 1) % (len(mapCache) - 1)) + 1]

        # see where we can actually move and execute all moves in tmpSpace; add to queue
        choices = [(1, 0), (0, 1), (0, 0), (-1, 0), (0, -1)]

        for yStep, xStep in choices:
            if ((0 < x + xStep < width - 1) and (0 <= y + yStep <= height - 1) and (tmpSpace[y + yStep][x + xStep] == ".")):
                # found possible new location
                newState = (clock, x + xStep, y + yStep)
                if newState not in visited:
                    visited[newState] = True
                    stateQueue.append(newState)

    return -1, -1


def solve(filename):
    file = open(filename)

    blocks = [line.rstrip() for line in file.read().split("\n")]

    blizzards = []
    width = len(blocks[0])
    height = len(blocks)
    s = blocks[len(blocks) - 1].rstrip()
    if s == "":
        height -= 1

    for y, s in enumerate(blocks):
        s = s.rstrip()
        for x, c in enumerate(s):
            if c in ["<", ">", "^", "v"]:
                b = Blizzard(c, x, y)
                blizzards.append(b)
            x += 1
        y += 1

    result1, result2 = bfs(1, 0, width, height, blizzards)
    return result1, result2


##########################
aocrunonce(24, True, True)
