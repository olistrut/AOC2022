import time
import numpy as numpy
from copy import deepcopy


class Transition:
    def __init__(self, name, source, dest, xFlip, yFlip, axisSwap, newDirection):
        self.name = name
        self.source = source
        self.dest = dest
        self.xFlip = xFlip
        self.yFlip = yFlip
        self.axisSwap = axisSwap
        self.newDirection = newDirection


def walk(x, y, space, display, direction, count):
    size = len(space)

    xStep = 0
    yStep = 0
    if direction in ["<", ">", "v", "^"]:
        display[y][x] = direction

        if direction == ">":
            xStep = 1
        elif direction == "<":
            xStep = -1
        elif direction == "^":
            yStep = -1
        elif direction == "v":
            yStep = 1
        for i in range(0, count):
            # do not need to check for 0 or width as field is enclosed by " " characters
            if space[(y + yStep)][(x + xStep)] == ".":
                # no wall, move
                x = (x + xStep)
                y = (y + yStep)

            elif space[(y + yStep)][(x + xStep)] == " ":
                # overrun
                yNew = y + yStep
                xNew = x + xStep
                if xStep > 0:
                    xNew = 0
                elif xStep < 0:
                    xNew = len(space) - 2
                elif yStep > 0:
                    yNew = 0
                elif yStep < 0:
                    yNew = len(space) - 2

                while space[(yNew + yStep)][(xNew + xStep)] == " ":
                    yNew += yStep
                    xNew += xStep
                cc = space[(yNew + yStep)][(xNew + xStep)]
                if space[(yNew + yStep)][(xNew + xStep)] == ".":
                    x = xNew + xStep
                    y = yNew + yStep
                else:
                    break
            else:
                break
            display[y][x] = direction

    return (y, x)


def showGrid(grid):
    return 0
    for row in grid:
        print("".join(c for c in row))


def solve1(filename):
    result1 = 0

    file = open(filename)
    elements = {}

    blocks = file.read().split("\n\n")
    command = blocks[1].rstrip()

    size = blocks[0].count("\n") + 10
    space = [[" " for i in range(size)] for j in range(size)]

    y = 1
    x = 1

    rows = 0
    cols = 0
    # setup grid
    lines = blocks[0].split("\n")
    for s in lines:
        x = 1

        for c in s:
            if c == "." or c == "#":
                space[y][x] = c
            x += 1

        y += 1

    display = deepcopy(space)
    showGrid((display))

    direction = ">"
    cmd = ""
    x = y = 0
    for i in range(len(space)):
        for j in range(len(space)):
            if space[i][j] != " ":
                x = j
                y = i
                break
        if x != 0:
            break

    for c in command:
        if c in ["R", "L"]:
            # change in direction
            count = int(cmd)
            # print("Walking ", count, " in direction ", direction)
            y, x = walk(x, y, space, display, direction, count)
            showGrid(display)
            result1 = y * 1000 + x * 4
            if direction == ">":
                result1 += 0
            elif direction == "v":
                result1 += 1
            elif direction == "<":
                result1 += 2
            elif direction == "^":
                result1 += 3

            if c == "R":
                if direction == ">":
                    direction = "v"
                elif direction == "v":
                    direction = "<"
                elif direction == "<":
                    direction = "^"
                elif direction == "^":
                    direction = ">"
            elif c == "L":
                if direction == ">":
                    direction = "^"
                elif direction == "^":
                    direction = "<"
                elif direction == "<":
                    direction = "v"
                elif direction == "v":
                    direction = ">"

            cmd = ""
        else:
            cmd += c

    count = int(cmd)
    # print("Walking ", count, " in direction ", direction)
    y, x = walk(x, y, space, display, direction, count)
    showGrid(display)
    result1 = y * 1000 + x * 4
    if direction == ">":
        result1 += 0
    elif direction == "v":
        result1 += 1
    elif direction == "<":
        result1 += 2
    elif direction == "^":
        result1 += 3

    return result1


def calcStep(direction):
    xStep = 0
    yStep = 0

    if direction == ">":
        xStep = 1
    elif direction == "<":
        xStep = -1
    elif direction == "^":
        yStep = -1
    elif direction == "v":
        yStep = 1

    return xStep, yStep


def cubeWalk(x, y, currentSquare, squares, transitions, displaySquares, direction, count):
    size = len(squares[0])

    # count = count % (size*4)

    square = squares[currentSquare]
    displaySquare = displaySquares[currentSquare]

    displaySquare[y][x] = direction

    xStep, yStep = calcStep(direction)

    for i in range(0, count):
        t = None
        if (y + yStep) == size:
            # y overrun
            t = transitions[currentSquare, "yOverflow"]
        elif (y + yStep) < 0:
            # y underrun
            t = transitions[currentSquare, "yUnderflow"]
        elif (x + xStep == size):
            # x overrun
            t = transitions[currentSquare, "xOverflow"]
        elif (x + xStep < 0):
            # x underrun
            t = transitions[currentSquare, "xUnderflow"]

        if t != None:
            # print("  Transition from cube ", currentSquare," to ", t.dest, " with direction ", direction)
            xTmp = x
            yTmp = y

            if t.axisSwap:
                yTmp = x
                xTmp = y

            if t.xFlip:
                xTmp = size - xTmp - 1
            if t.yFlip:
                yTmp = size - yTmp - 1

            if squares[t.dest][yTmp][xTmp] == ".":
                x = xTmp
                y = yTmp
                square = squares[t.dest]
                displaySquare = displaySquares[t.dest]
                direction = t.newDirection
                xStep, yStep = calcStep(direction)
                currentSquare = t.dest
            else:
                break


        else:
            if square[(y + yStep)][(x + xStep)] == ".":
                # no wall, move
                x = (x + xStep)
                y = (y + yStep)
            elif square[(y + yStep)][(x + xStep)] == "#":
                # wall - stop moving
                break

        displaySquare[y][x] = direction

    return (y, x, currentSquare, direction)


def setupTransitions(shape):
    transitions = {}
    if shape == 1:
        transitions[(0, "xOverflow")] = Transition("xOverflow", 0, 5, False, True, False, "<")
        transitions[(0, "xUnderflow")] = Transition("xUnderflow", 0, 2, False, False, True, "v")  # 1
        transitions[(0, "yOverflow")] = Transition("yOverflow", 0, 3, False, True, False, "v")
        transitions[(0, "yUnderflow")] = Transition("yUnderflow", 0, 1, True, False, False, "v")

        transitions[(1, "xOverflow")] = Transition("xOverflow", 1, 2, True, False, False, ">")
        transitions[(1, "xUnderflow")] = Transition("xUnderflow", 1, 5, True, True, True, "^")
        transitions[(1, "yOverflow")] = Transition("yOverflow", 1, 4, True, False, False, "^")  # 4
        transitions[(1, "yUnderflow")] = Transition("xOverflow", 1, 0, True, False, False, "v")  # 0

        transitions[(2, "xOverflow")] = Transition("xOverflow", 2, 3, True, False, False, ">")
        transitions[(2, "xUnderflow")] = Transition("xUnderflow", 2, 1, True, False, False, "<")
        transitions[(2, "yOverflow")] = Transition("yOverflow", 2, 4, True, True, True, ">")
        transitions[(2, "yUnderflow")] = Transition("yUnderflow", 2, 0, False, False, True, ">")

        transitions[(3, "xOverflow")] = Transition("xOverflow", 3, 5, True, True, True, "v")
        transitions[(3, "yOverflow")] = Transition("yOverflow", 3, 4, False, True, False, "v")
        transitions[(3, "yUnderflow")] = Transition("yUnderflow", 3, 0, False, True, False, "^")
        transitions[(3, "xUnderflow")] = Transition("xUnderflow", 3, 2, True, False, False, "<")

        transitions[(5, "xOverflow")] = Transition("xOverflow", 5, 0, False, True, False, "<")
        transitions[(5, "xUnderflow")] = Transition("xUnderflow", 5, 4, True, False, False, "<")
        transitions[(5, "yOverflow")] = Transition("yOverflow", 5, 1, True, True, True, ">")
        transitions[(5, "yUnderflow")] = Transition("yUnderflow", 5, 3, True, True, True, "<")

        transitions[(4, "xUnderflow")] = Transition("xUnderflow", 4, 2, True, True, True, "^")
        transitions[(4, "xOverflow")] = Transition("xOverflow", 4, 5, True, False, False, ">")
        transitions[(4, "yOverflow")] = Transition("yOverflow", 4, 1, True, False, False, "^")
        transitions[(4, "yUnderflow")] = Transition("yOverflow", 4, 3, False, True, False, "^")
    elif shape == 2:
        transitions[(0, "xOverflow")] = Transition("xOverflow", 0, 1, True, False, False, ">")
        transitions[(0, "yOverflow")] = Transition("yOverflow", 0, 2, False, True, False, "v")
        transitions[(0, "xUnderflow")] = Transition("xUnderflow", 0, 3, False, True, False, ">")
        transitions[(0, "yUnderflow")] = Transition("yUnderflow", 0, 5, False, False, True, ">")

        transitions[(1, "xUnderflow")] = Transition("xUnderflow", 1, 0, True, False, False, "<")
        transitions[(1, "xOverflow")] = Transition("xOverflow", 1, 4, False, True, False, "<")
        transitions[(1, "yOverflow")] = Transition("yOverflow", 1, 2, False, False, True, "<")
        transitions[(1, "yUnderflow")] = Transition("xOverflow", 1, 5, False, True, False, "^")  # 0

        transitions[(2, "yUnderflow")] = Transition("yUnderflow", 2, 0, False, True, False, "^")
        transitions[(2, "yOverflow")] = Transition("yOverflow", 2, 4, False, True, False, "v")
        transitions[(2, "xUnderflow")] = Transition("xUnderflow", 2, 3, False, False, True, "v")
        transitions[(2, "xOverflow")] = Transition("xOverflow", 2, 1, False, False, True, "^")

        transitions[(3, "xOverflow")] = Transition("xOverflow", 3, 4, True, False, False, ">")
        transitions[(3, "yOverflow")] = Transition("yOverflow", 3, 5, False, True, False, "v")
        transitions[(3, "xUnderflow")] = Transition("xUnderflow", 3, 0, False, True, False, ">")
        transitions[(3, "yUnderflow")] = Transition("xUnderflow", 3, 2, False, False, True, ">")

        transitions[(4, "xUnderflow")] = Transition("xUnderflow", 4, 3, True, False, False, "<")
        transitions[(4, "yUnderflow")] = Transition("yOverflow", 4, 2, False, True, False, "^")
        transitions[(4, "xOverflow")] = Transition("xOverflow", 4, 1, False, True, False, "<")
        transitions[(4, "yOverflow")] = Transition("yOverflow", 4, 5, False, False, True, "<")

        transitions[(5, "yUnderflow")] = Transition("yOverflow", 5, 3, False, True, False, "^")
        transitions[(5, "xOverflow")] = Transition("xOverflow", 5, 4, False, False, True, "^")
        transitions[(5, "yOverflow")] = Transition("yOverflow", 5, 1, False, True, False, "v")
        transitions[(5, "xUnderflow")] = Transition("xUnderflow", 5, 0, False, False, True, "v")

    return transitions


def showCube(squares):
    for i, s in enumerate(squares):
        print("==>> Square: ", i)
        for row in s:
            print("".join(c for c in row))
            pass


def solve2(filename, shape):
    result1 = 0

    file = open(filename)

    blocks = file.read().split("\n\n")
    command = blocks[1].rstrip()

    count = 0
    for row in blocks[0].split('\n'):
        if (0 < row.count(".") + row.count("#") < count) or (count == 0):
            count = row.count(".") + row.count("#")
    size = count
    space = [[" " for i in range(size * 5)] for j in range(size * 5)]

    squares = []

    y = 0
    x = 0

    lines = blocks[0].split("\n")
    for s in lines:
        x = 0
        for c in s:
            if c != " ":
                space[y][x] = c
            x += 1
        y += 1

    space = numpy.array(space)
    transitions = setupTransitions(shape)
    squareCoordinates = []
    if shape == 1:
        # y/x
        squareCoordinates.append((0, 2))
        squareCoordinates.append((1, 0))
        squareCoordinates.append((1, 1))
        squareCoordinates.append((1, 2))
        squareCoordinates.append((2, 2))
        squareCoordinates.append((2, 3))

    elif shape == 2:
        # y/x
        squareCoordinates.append((0, 1))
        squareCoordinates.append((0, 2))
        squareCoordinates.append((1, 1))
        squareCoordinates.append((2, 0))
        squareCoordinates.append((2, 1))
        squareCoordinates.append((3, 0))

    squares = []
    for i in range(6):
        x = squareCoordinates[i][1]
        y = squareCoordinates[i][0]
        squares.append(space[y * size:(y + 1) * size, x * size:(x + 1) * size])

    direction = ">"

    displaySquares = deepcopy(squares)
    # set starting position
    # always starting at 0,0 in square 0

    x = y = 0
    currentSquare = 0

    c = command[0]
    commandPos = 0
    cmd = ""

    while (True):
        if c in ["R", "L", "X"]:
            count = int(cmd)
            # print("Walking ", count, " in direction ", direction, " in square ", currentSquare)
            y, x, currentSquare, direction = cubeWalk(x, y, currentSquare, squares, transitions, displaySquares, direction, count)
            cmd = ""

            if c == "R":
                if direction == ">":
                    direction = "v"
                elif direction == "v":
                    direction = "<"
                elif direction == "<":
                    direction = "^"
                elif direction == "^":
                    direction = ">"
            elif c == "L":
                if direction == ">":
                    direction = "^"
                elif direction == "^":
                    direction = "<"
                elif direction == "<":
                    direction = "v"
                elif direction == "v":
                    direction = ">"
            elif c == "X":
                break
        else:
            cmd += c

        commandPos += 1
        if commandPos < len(command):
            c = command[commandPos]
        else:
            c = "X"

    # position and direction in square -> translate back to overall
    y = size * squareCoordinates[currentSquare][0] + y + 1  # +1 to account for task 22 coordinate system starting at 1
    x = size * squareCoordinates[currentSquare][1] + x + 1

    result1 = 1000 * y + 4 * x
    if direction == ">":
        result1 += 0
    elif direction == "v":
        result1 += 1
    elif direction == "<":
        result1 += 2
    elif direction == "^":
        result1 += 3
    return result1


start = time.time()
filename = "input/input22-sample.txt"
p1  = solve1(filename)
print ("Part 1 (Example): ", p1)
p2 = solve2(filename, 1)
print ("Part 2 (Example): ", p2)


filename = "input/input22.txt"
p2 = solve2(filename, 2)
p1 = solve1(filename)
print ("Part 1 (Data): ", p1)
print("Part 2 (Data): ", p2)

print("Total time: ", round(time.time()-start, 3))