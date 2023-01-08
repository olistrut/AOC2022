exec(open("aochelper.py").read())

def sign(x):
    return (x > 0) - (x < 0)


def solve(filename, **kwargs):
    maxElem = kwargs["maxelem"]-1
    visualization = False
    visual = {}
    result = 0
    file = open(filename)

    maxX = 0
    maxY = 0
    minX = 0
    minY = 0

    tailPos = set()
    # store x and y coordinates; x[0] = Head; x[maxElem] = Tail
    lines = file.read().split("\n")
    lines = [line.rstrip() for line in lines]
    lines = list(filter(None, lines))
    size = 50
    x = (maxElem + 1) * [int(size / 2)]
    y = (maxElem + 1) * [int(size / 2)]

    if (visualization):
        visual[(x[0],y[0])] = "S"
        maxX = max(maxX, x[0])
        maxY = max(maxY, y[0])
        minX = max(minX, x[0])
        minY = max(minY, y[0])


    for s in lines:
        dir, step = s.split(" ")
        step = int(step)

        for i in range(step):

            # print ("Moving ", dir, " - step ", i, " of ",step)

            # Move the head
            if (dir == "R"):
                x[0] += 1
            elif (dir == "L"):
                x[0] -= 1
            elif (dir == "U"):
                y[0] -= 1
            elif (dir == "D"):
                y[0] += 1
            else:
                print("Error: undefined direction (", dir, ")")

            for j in range(maxElem):
                distX = x[j] - x[j + 1]
                distY = y[j] - y[j + 1]

                if (abs(distX) == 2):
                    x[j + 1] += sign(distX)
                    if (abs(distY) == 1):
                        y[j + 1] += sign(distY)

                if (abs(distY) == 2):
                    y[j + 1] += sign(distY)
                    if (abs(distX) == 1):
                        x[j + 1] += sign(distX)

            if visualization:
                visual[(x[j + 1],y[j + 1])] = 'T'
                maxX = max(maxX, x[j+1])
                maxY = max(maxY, y[j+1])
                minX = min(minX, x[j+1])
                minY = min(minY, y[j+1])

            # keep a set of unique positions of "T"
            tailPos.add(str(y[j + 1]) + "-" + str(x[j + 1]))

    if (visualization):
      for y in range(minY-2, maxY+2):
        for x in range(minY-2, maxX+2):
          if (x,y) in visual:
              print (visual[(x,y)], end = "")
          else:
              print(".", end = "")
        print()

    result = len(tailPos)
    return result

#########################
aocruntwice(9, True, True, {"maxelem":2}, {"maxelem":10})
