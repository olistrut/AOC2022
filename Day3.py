import time

def count(s):
    result = 0
    for c in s:
        if (c.islower()):
            result += ord(c) - 96
        else:
            result += ord(c) - 64 + 26

    return result


def solve(filename):

    file = open(filename)

    result1 = 0
    result2 = 0
    lines = [line.rstrip() for line in file.readlines()]

    for s in lines:
        l = len(s)

        intersect = set(s[0:int(l / 2)]).intersection(set(s[int(l / 2):l]))
        result1 += count(intersect)


    # part 2
    v = 0
    for i in range(0, int(len(lines) / 3)):
        s1 = set(lines[i * 3])
        s2 = set(lines[i * 3 + 1])
        s3 = set(lines[i * 3 + 2])

        intersect = s1.intersection(s2, s3)
        result2 += count(intersect)

    return result1, result2

start = time.time()
filename = "input/input3-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input3.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)
print("Total time: ", round(time.time()-start, 2))