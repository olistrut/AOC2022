import time
from copy import deepcopy


def create_stack(stackData):
    # stacks are in reverse order; stack[0] represents the bottom of the stack
    stack = []

    *crates, numRow = stackData.split("\n")
    cols = len(numRow.split())

    for line in crates:
        n = round(len(line) / cols)
        columns = [line[i:i + n] for i in range(0, len(line), n)]

        i = 0
        for i, element in enumerate(columns):
            element = element.replace('[', '').replace(']', '').rstrip()

            if (i >= len(stack)):
                stack.append([])

            if (element != ""):
                stack[i].append(element)

    return stack


def reshuffle(commandData, stack, part):
    result = ""

    for cmd in commandData.split("\n"):
        if len(cmd := cmd.rstrip()) > 0:
            cmd = cmd.split(" ")

            num = int(cmd[1])
            source = int(cmd[3])
            dest = int(cmd[5])

            for i in range(0, num):
                if 1 == part:
                    index = 0
                else:
                    index = num - i - 1
                stack[dest - 1].insert(0, stack[source - 1].pop(index))

    for i in (stack):
        result = result + i[0]
    return result


def solve(filename):
    file = open(filename)
    stackData, commandData = file.read().split("\n\n")

    stack = create_stack(stackData)
    result1 = reshuffle(commandData, deepcopy(stack), 1)
    result2 = reshuffle(commandData, deepcopy(stack), 2)

    return result1, result2


start = time.time()

filename = "input/input5-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example):', p2)

filename = "input/input5.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data):', p2)

print("Total time: ", round(time.time() - start, 3))
