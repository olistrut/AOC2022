exec(open("aochelper.py").read())

def solve(filename):
    forest = []
    file = open(filename)
    while (s := file.readline().rstrip('\n')):
        forest.append(list(map(int, s)))

    result1 = result2 = 0

    for i in range(0, len(forest)):
        for j in range(0, len(forest[i])):
            distanceLeft = distanceRight = distanceAbove = distanceBelow = 0
            leftVisible = aboveVisible = rightVisible = belowVisible = True

            h = forest[i][j]

            for row in (range(i - 1, -1, -1)):
                distanceAbove += 1
                if (h <= forest[row][j]):
                    aboveVisible = False
                    break

            for row in (range(i + 1, len(forest))):
                distanceBelow += 1
                if (h <= forest[row][j]):
                    belowVisible = False
                    break

            for col in (range(j - 1, -1, -1)):
                distanceLeft += 1
                if (h <= forest[i][col]):
                    leftVisible = False
                    break

            for col in (range(j + 1, len(forest[i]))):
                distanceRight += 1
                if (h <= forest[i][col]):
                    rightVisible = False
                    break

            result1 += int(leftVisible or rightVisible or aboveVisible or belowVisible)
            result2 = max(distanceLeft * distanceRight * distanceAbove * distanceBelow, result2)

    return result1, result2

#####################
aocrun(8, True, True)

