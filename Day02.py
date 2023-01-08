import time

def solve(filename):
    result1 = 0
    result2 = 0

    f = open(filename)

    results = {
        ("A", "X"): (4, 3),
        ("A", "Y"): (8, 4),
        ("A", "Z"): (3, 8),
        ("B", "X"): (1, 1),
        ("B", "Y"): (5, 5),
        ("B", "Z"): (9, 9),
        ("C", "X"): (7, 2),
        ("C", "Y"): (2, 6),
        ("C", "Z"): (6, 7)

    }

    while s := f.readline():
        challenge, response = s.split()
        r = results[(challenge, response)]
        result1 += r[0]
        result2 += r[1]

    return result1, result2


start = time.time()
filename = "input/input2-sample.txt"
p1, p2 = solve(filename)
print("Part 1 (Example): ", p1)
print('Part 2 (Example): ', p2)

filename = "input/input2.txt"
p1, p2 = solve(filename)
print("Part 1 (Data): ", p1)
print('Part 2 (Data): ', p2)
print("Total time: ", time.time() - start)
