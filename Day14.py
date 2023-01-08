exec(open("aochelper.py").read())
from collections import defaultdict

def drop(y, x, grid, height):
  while (y <= height and (grid.get((x,y), "None")!= "o")):
    if (not (x,y+1) in grid) :
      y = y+1
    elif not (x-1,y+1) in grid :
      x = x-1
      y = y+1
    elif not (x + 1, y + 1) in grid:
      x = x+1
      y = y+1
    else:
      grid[(x,y)] = "o"
      return False
  return True

def solve(filename):
  result1 = 0
  result2 = 0
  height = 800
  width = 1000
  grid = {}

  maxY = 0

  file = open(filename)
  while (line:=file.readline().rstrip()):
    coords = line.split(" -> ")
    x1, y1 = map(int, coords[0].split(","))
    for i in range(1,len(coords)):
      x2, y2 = map(int, coords[i].split(","))
      maxY = max(maxY, y1, y2)
      if (x2 != x1):
        for x in range(min(x1, x2), max(x1+1,x2+1)):
          grid[(x,y1)] = "X"

      elif (y2 != y1):
        for y in range(min(y1, y2), max(y1+1,y2+1)):
          grid[(x1,y)] = "X"

      x1 = x2
      y1 = y2

  while (not drop(0, 500, grid, maxY)):
    result1 += 1

  for x in range(0,width):
    grid[( x, maxY + 2)] = "X"

  while (not drop(0, 500, grid, maxY+1)):
    result2 += 1

  result2 += result1

  return result1, result2


######################################################################################
aocrunonce(14, True, True)

