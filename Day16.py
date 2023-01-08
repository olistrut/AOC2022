exec(open("aochelper.py").read())

class Valve:
  def __init__(self, name, rate, neighbours):
    self.name = name  # instance variable unique to each instance
    self.rate = rate
    self.neighbours = neighbours

  def __str__(self):
    s = "Name: "+self.name+" - Rate: "+self.rate + " - Neighbors: "
    for n in self.neighbours:
      s += n+" "
    return s

nonZeroNodes = []

def dfs1 (start, valves, opened, length, rate, predecessor):
  if length ==  30:
    return rate

  # ugly optimization
  if (length > 9 and rate < 600):
    return rate
  if (length > 20 and rate <= 1200):
    return rate

  if (len(opened) == len(nonZeroNodes)):
    return rate

  pressure = rate

  v = valves[start]

  for n in v.neighbours:
      if not v.name in opened and v.rate > 0:
        # new node v is an active and unopened valve

        # try opening
        opened[v.name] = length
        if length < 29: pressure = max(pressure, dfs1(n, valves, opened, length + 2, rate+ v.rate * (30 - length ), start))
        del opened[v.name]

        # and try just moving on
        if (predecessor != n): pressure = max(pressure, dfs1(n, valves, opened, length + 1, rate, start))

      elif v.rate == 0:
        # new node v is a broken valve - no point opening, just move on
        if (predecessor != n):
          # don't directly go back from 0 valve to predecessor
          pressure = max(pressure, dfs1(n, valves, opened, length + 1, rate, start))
      else:
        # valve is already open, just move on
        if (predecessor != n):
          # don't directly go back from 0 valve to predecessor
          pressure = max(pressure, dfs1(n, valves, opened, length + 1, rate, start))

  return pressure


currentBestRate = 0
currentBestRateTimeToOpenAll = 27

visited = {}

def dfs2 (starts, valves, opened, paths, minute, rate, storedRate):
  global currentBestRate
  global currentBestRateTimeToOpenAll
  global visited

  if minute == 26:
    return rate

  start1 = starts[0]
  start2 = starts[1]

  stateString = str(opened) + str(start1) +"-"+str(start2) + str(minute)
  if stateString in visited :
    if visited[stateString] >= rate:
      return rate
    else:
      visited[stateString] = rate
      stateString = str(opened) + str(start2) + "-" + str(start1) + str(minute)
      visited[stateString] = rate
  else:
      visited[stateString] = rate
      stateString = str(opened) + str(start2) + "-" + str(start1) + str(minute)
      visited[stateString] = rate

  if minute > currentBestRateTimeToOpenAll +1  and rate < currentBestRate:
    return rate

  # if no change over last 5 steps, terminate this path
  if (minute > 1 and minute % 5 == 0 and rate == storedRate):
    return rate
  elif minute % 5 == 0 and rate != storedRate:
    storedRate = rate

  # ugly optimization
  if (minute >8 and rate < 1300):
    return rate
  if (minute > 15 and rate <= 2200):
    return rate

  pressure = rate

  v1 = valves[start1]
  v2 = valves[start2]

  path1 = list(paths[0])
  path2 = list(paths[1])

  path1.append(start1)
  path2.append(start2)

  # useless loops
  if (len(path2)>=3 and (path2[-3]==path2[-1])):
    if path2[-2] not in opened:
     return rate
    elif opened[path2[-2]] != len(path2)-2:
      return rate

  if (len(path1)>=3 and (path1[-3]==path1[-1])):
    if path1[-2] not in opened:
     return rate
    elif opened[path1[-2]] != len(path1)-2:
      return rate

  # end branch if all valves are open and store time/rate for future bounding of branches
  if (len(opened) == len(nonZeroNodes)): # all non zero valves are open
    if rate > currentBestRate:
      currentBestRate = rate
      currentBestRateTimeToOpenAll = minute
    return rate


  for i in range(-1, len(v1.neighbours)):
    for j in range(len(v2.neighbours)-1, -2, -1): # prefer to run in different directions earlier
      if (i == -1 or j == -1) and minute == 1: continue # assumes AA has flow rate of 0
      if (v1 == v2) and (i == -1 and j == -1): continue
      if (v1.rate == 0 and i == -1) or v2.rate == 0 and j == -1: continue # it doesn't make sense for either party to attempt to open valve if rate = 0

      tmpRate = rate
      n1 = start1
      n2 = start2
      added1 = False
      added2 = False

      if i == -1:
        # open valve
        if (not v1.name in opened) and v1.rate > 0:
          opened[v1.name] = minute
          tmpRate = tmpRate +  v1.rate * (26 - minute )
          added1 = True
        else:
          # valve already open or zero-valve
          added1 = False
      else:
        # move
        n1 = v1.neighbours[i]

      if j == -1:
        # open valve
        if (not v2.name in opened)  and v2.rate > 0:
          opened[v2.name] = minute
          tmpRate = tmpRate +  v2.rate * (26 - minute )
          added2 = True
        else:
          # valve already open or zero-valve
          added2 = False
      else:
        # move
        n2 = v2.neighbours[j]

      skip = False
      # various optimizations
      # no movement for 3 steps (2 steps is ok because we might just open the valve)
      if n1 == path1[-1] == path1[-2]:
        skip = True
      if n2 == path2[-1] == path2[-2]:
        skip = True
      # no movement for 2 steps and no valve added to opened list
      if added2==False and n2 == path2[-1]:
        skip = True
      if added1==False and n1 == path1[-1]:
        skip = True

      if not skip: pressure = max(pressure, dfs2([n1, n2], valves, opened, [path1, path2], minute+1, tmpRate, storedRate))

      if added1:
          del opened[v1.name]
      if added2:
          del opened[v2.name]


  path1.pop()
  path2.pop()

  return pressure


def solve(filename):
  result1 = 0
  result2 = 0

  valves = {}

  file = open(filename)

  while (line:=file.readline().rstrip()):
    tokens = line.split(" ")
    neighbours = tokens[9:]
    neighbours = [n.strip(',') for n in neighbours]
    v = Valve(tokens[1], int(tokens[4].split("=")[1].split(";")[0]), neighbours)
    valves[v.name] = v
    if v.rate != 0: nonZeroNodes.append(v.name)

  result1 = dfs1("AA", valves, {},  1,0, 0)
  global visited
  visited = {}
  result2 = dfs2(["AA", "AA"], valves, {}, [[], []],  1,0, 0)

  return result1, result2


#####################################
aocrunonce(16, True, True)
