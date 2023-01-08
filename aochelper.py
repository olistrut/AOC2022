import time

# same param for p1 and p2 and example and data
def aocrunonce(day, runExample, runData, args = {}):
    start = time.time()

    if runExample:
        filename = "input/input"+str(day)+ "-sample.txt"
        p1, p2 = solve(filename, **args)
        print ("Part 1 (Example): ", p1)
        print ('Part 2 (Example):', p2)

    if runData:
        filename = "input/input"+str(day)+".txt"
        p1, p2 = solve(filename, **args)
        print ("Part 1 (Data): ", p1)
        print ('Part 2 (Data):', p2)

    print("Total time: ", round(time.time()-start, 3))

# different params for p1 and p2
def aocruntwice(day, runExample, runData, r1 = {}, r2 = {}):
    start = time.time()

    if runExample:
        filename = "input/input"+str(day)+ "-sample.txt"
        p1 = solve(filename, **r1)
        p2 = solve(filename, **r2)

        print ("Part 1 (Example): ", p1)
        print ('Part 2 (Example):', p2)

    if runData:
        filename = "input/input"+str(day)+".txt"
        p1 = solve(filename, **r1)
        p2 = solve(filename, **r2)
        print ("Part 1 (Data): ", p1)
        print ('Part 2 (Data):', p2)

    print("Total time: ", round(time.time()-start, 3))

def aocrunwithdataparams(day, runExample, runData, exampleparam = {}, dataparam = {}):
    start = time.time()

    if runExample:
        filename = "input/input"+str(day)+ "-sample.txt"
        p1, p2 = solve(filename, **exampleparam)

        print ("Part 1 (Example): ", p1)
        print ('Part 2 (Example):', p2)

    if runData:
        filename = "input/input"+str(day)+".txt"
        p1, p2 = solve(filename, **dataparam)
        print ("Part 1 (Data): ", p1)
        print ('Part 2 (Data):', p2)

    print("Total time: ", round(time.time()-start, 3))

def aocrundifferentfunctions(day, runExample, runData):
    start = time.time()

    if runExample:
        filename = "input/input"+str(day)+ "-sample.txt"
        p1 = solve1(filename)
        p1 = solve2(filename)

        print ("Part 1 (Example): ", p1)
        print ('Part 2 (Example):', p2)

    if runData:
        filename = "input/input"+str(day)+".txt"
        p1 = solve1(filename)
        p1 = solve2(filename)
        print ("Part 1 (Data): ", p1)
        print ('Part 2 (Data):', p2)

    print("Total time: ", round(time.time()-start, 3))
