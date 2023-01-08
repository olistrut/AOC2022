import time


def solve(filename):
    result2 = 0
    result1 = 0
    file = open(filename)
    while (s := file.readline().rstrip()):
        s1, s2 = s.split(',')
        min1, max1 = map(int, (s1.split('-')))
        min2, max2 = map(int, (s2.split('-')))

        if ((min1 <= min2) and (max1 >= max2)):
            result1 += 1
        elif (min2 <= min1) and (max2 >= max1):
            result1 += 1

        if ((min1 <= min2) and (max1 >= min2)):
            result2 += 1
        elif (min2 <= min1) and (max2 >= min1):
            result2 += 1

    return result1, result2


start = time.time()
filename = "input/input4-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print("Part 2 (Example): ", p2)

filename = "input/input4.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data):', p2)
print("Total time: ", round(time.time() - start, 3))
