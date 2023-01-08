exec(open("aochelper.py").read())

from collections import deque

def bfs(x, y, width, height, length, map):
  queue = deque()
  visited = {}
  queue.append((y,x,0,""))
  visited[(x,y)] = True

  while len(queue) > 0:
    y, x, depth, path = queue.popleft()
    if(map[y][x]) == chr(123):
      return depth

    neighbours = []

    if (y < height - 1):
      neighbours.append((0,1, "v"))
    if (y > 0):
      neighbours.append((0,-1, "^"))
    if (x > 0):
      neighbours.append((-1,0, "<"))
    if (x<width-1):
      neighbours.append((+1, 0, ">"))

    for (xStep, yStep, step) in neighbours:
      if (ord(map[y +yStep][x+xStep]) <= ord(map[y][x]) + 1 or (map[y][x] == "y" and map[y + yStep][x+xStep] == chr(123))):
        if not (x+xStep,y+yStep) in visited:
          queue.append((y+yStep,x+xStep, depth+1, path+step))
          visited[(x+xStep,y+yStep)] = True

  return(width * height +1 )

def solve(filename):
  result1 = 0
  result2 = 0

  map = []
  visited = []

  file = open(filename)

  y = x = row = 0
  while (s:=file.readline().rstrip()):

    if (s.find("S")>=0):
       y = row
       x = s.find("S")
    s = s.replace("S", "a")
    s = s.replace("E",chr(123))

    map.append(list(s))
    row+=1

  width = len(map[0])
  height = len(map)

  result2 = width * height

  # Breadth first search
  result1 =  bfs(x, y, width, height, 0, map)

  for y in range(len(map)):
    for x in range(len(map[y])):
      if (map[y][x] == "a"):
        result2 = min(result2, bfs(x, y, width, height, 0, map))

  return result1, result2

######################################################################################
aocrunonce(12, True, True)



