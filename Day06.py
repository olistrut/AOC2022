import time


def findUniqueChars(input, length):
    for i in range(0, len(input) - length + 1):
        if (len(set(input[i:i + length])) == length):
            return i + length


def solve(filename):
    file = open(filename)
    input = file.readline()
    # input="mjqjpqmgbljsphdztnvjfqwrcgsmlb"

    # part 1
    result1 = findUniqueChars(input, 4)

    # part 2
    result2 = findUniqueChars(input, 14)

    return result1, result2


start = time.time()
filename = "input/input6.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data):', p2)
print("Total time: ", round(time.time() - start, 3))
