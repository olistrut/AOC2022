exec(open("aochelper.py").read())

from collections import deque

def buildExterior (space, size):
  exterior = {}
  visited = {}
  queue = deque()
  queue.append((0,0,0))

  neighbours = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

  while (len(queue)>0):
    (x,y,z) = queue.popleft()
    if not (x,y,z) in visited:
      if not (x, y, z) in exterior: exterior[(x, y, z)] = True
      visited[(x,y,z)] = True

      for nx, ny, nz in neighbours:
          coords = (x + nx, y + ny, z+nz)
          if not coords in space and coords[0]>=-1 and coords[1]>=-1 and coords[2]>=-1 and coords[0]<= size and coords[1]<= size and coords[2] <= size:
              queue.append(coords)

  return exterior

def solve(filename):
  result1 = 0
  result2 = 0

  file = open(filename)

  space = {}
  size = 0

  while s:= file.readline().rstrip():
    x, y, z = map(int, s.split(","))
    size = max(size, x,y,z)
    space[(x,y,z)] = "#"

  exterior = buildExterior(space, size)
  neighbours = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

  for (x,y,z) in space:
          for nx, ny, nz in neighbours:
                coords = (x + nx, y + ny, z + nz)
                if not coords in space:
                    result1 += 1
                    if coords in exterior:
                        result2 += 1

  return result1, result2

###################################################################################
aocrunonce(18, True, True)



