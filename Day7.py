import time

def solve(filename):
    file = open(filename)

    result1 = 0
    result2 = 0

    stack = [0]
    sizelist = []
    totalsize = 0

    sizelimit = 100000

    while len(stack)>0:
      if not (line:=file.readline()):
        # if we are at the end of the input file, bubble up to top level
        line = "$ cd .."

      if line.startswith("$ cd /"):
        # no handling of "cd /" in the middle of the command list; that did not happen in either sample file nor my aoc input, so ignored this edge case
        # would have to bubble back up to an empty stack (and count sizes along the way)
        pass
      elif line.startswith("$ cd .."):
        dirsize = stack.pop()
        sizelist.append(dirsize)
        if (dirsize<=sizelimit):
          result1 += dirsize
        if len(stack) > 0: stack[-1] += dirsize
      elif line.startswith("$ cd "):
        stack.append(0)
      elif (line[0].isdigit()):
        size = int(line[0:line.find(" ")])
        stack[-1] += size
        totalsize += size

    # part 2
    freespace = 70000000 - totalsize
    todelete = 30000000 - freespace

    # find smallest dir sufficiently large to delete
    result2 = min(size for size in sizelist if size >= todelete)
    return result1, result2


start = time.time()
filename = "input/input7-sample.txt"
p1, p2 = solve(filename)
print ("Part 1 (Example): ", p1)
print ('Part 2 (Example):', p2)

filename = "input/input7.txt"
p1, p2 = solve(filename)
print ("Part 1 (Data): ", p1)
print ('Part 2 (Data):', p2)
print("Total time: ", round(time.time()-start, 3))
