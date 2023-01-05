import time

def solve(filename):
    file = open(filename)
    blocks = file.read().split("\n\n")
    cals = []

    for block in blocks:
        cal= sum(list(map(int, block.rstrip().split("\n"))))
        cals.append(cal)

    cals = sorted(cals)
    return max(cals),sum(cals[-3:])

start = time.time()
filename = "input/input1-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input1.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)
print("Total time: ", time.time()-start)