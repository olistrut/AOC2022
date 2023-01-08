exec(open("aochelper.py").read())

def countActiveRows(grid):
  rowCount = 0
  for i in range(len(grid)):
    if (grid[i].find("#") >= 0):
      rowCount += 1
  return rowCount

def getShape(id):
  if id == 0:
    return ["..@@@@."]
  elif (id == 1):
    return  ["...@...","..@@@..","...@..."]
  elif (id == 2):
    return ["..@@@..", "....@..","....@.."]
  elif (id == 3):
    return ["..@....", "..@....", "..@....", "..@...."]
  elif (id == 4):
    return ["..@@...", "..@@..."]


def solve(filename, **kwargs):
  iterations = kwargs["iterations"]
  result = 0
  width = 7

  deleted = 0

  file = open(filename)
  grid = []

  states = {}

  blockCount = 0
  pos = 0
  command = file.readline().rstrip()

  periodStart = None
  currentHeight = 0
  periodIdentified = False

  while (blockCount < iterations):
    # ensure we have 3 empty lines at top
    grid.append(".......")
    grid.append(".......")
    grid.append(".......")

    empties = 0
    while (grid[-empties-1].count(".") == width):
      empties += 1
      if empties >= len(grid): break
    if (empties > 3):
      while (empties > 3):
        grid.pop()
        empties -= 1

    shape = getShape(blockCount % 5)
    spriteHeight = len(shape)
    grid.extend(shape)
    spriteTop = len(grid)
    spriteBottom = spriteTop - spriteHeight
    intersect = False
    jet = True
    lastRow = 0
    bump = False

    while (not intersect):
      firstRow = False

      tmpGrid = grid.copy()
      bump = False

      if (jet == True):

        if command[pos % len(command)] == "<":
            #for y in range(spriteTop, spriteBottom-1, -1):
            for y in range(spriteTop-1, spriteBottom-1, -1):
              for x in range(0, width):
                if grid[y].rfind("@") > 0: # avoid out of bounds
                  if (grid[y][x] == "@"):
                    if(tmpGrid[y][x-1] == "."):
                      tmpGrid[y] = tmpGrid[y][:x-1]+"@."+tmpGrid[y][x+1:]
                    else:
                      bump = True
                else:
                  bump = True

        elif command[pos % len(command)] ==">":
            for y in range(spriteTop-1, spriteBottom-1, -1):
              for x in range(width-1, -1, -1):
                if grid[y].rfind("@") < 6: # avoid out of bounds
                  if (grid[y][x] == "@"):
                    if(tmpGrid[y][x+1] == "."):
                      tmpGrid[y] = tmpGrid[y][:x]+".@"+tmpGrid[y][x+2:]
                    else:
                      bump = True
                else:
                  bump = True

        pos += 1

      else: # drop
          #print("Dropping")
          for y in range(spriteBottom, spriteTop):
            for x in range(0, width):
              if (grid[y].find("@") >= 0 and y == 0):
                # hit bottom
                intersect = True
                break
              else:
                if (grid[y][x] == "@"):
                  if (tmpGrid[y-1][x] == "."):
                    tmpGrid[y-1] = tmpGrid[y-1][:x]+"@"+tmpGrid[y-1][x+1:]
                    tmpGrid[y] = tmpGrid[y][:x]+"."+tmpGrid[y][x+1:]
                  else:
                    intersect = True
                    break
            if(intersect): break
          if not (intersect):
            spriteTop -= 1
            spriteBottom -= 1

      if (not intersect) and (not bump):
          grid = tmpGrid.copy()
      elif (intersect):
        # hit an intersection with the bottom or another brick. blocks now in place. replace @ with X#
        for i in range(spriteBottom, spriteTop):
          grid[i] = grid[i].replace("@", "#")

        # find periodicity
        # identifying string created from top 25 lines of the grid
        if len(grid) >100:
          s = str(grid[-25:])
          rowCount = countActiveRows(grid)

          if s in states and not periodIdentified:
            # we found a period
            # calculate incremental  lines and blocks for this iteration

            currentHeight = countActiveRows(grid)

            periodStart = states[s]
            periodHeight = currentHeight - periodStart[0]
            periodBlocks = blockCount - periodStart[1]
            remainingFullRounds = (iterations - blockCount) // periodBlocks
            result = currentHeight + remainingFullRounds * periodHeight
            blockCount = blockCount + remainingFullRounds * periodBlocks
            periodIdentified = True

          else:
            states[s] = (rowCount, blockCount)

      jet = not jet

    blockCount += 1

  return result + countActiveRows(grid) - currentHeight

###########################################################
aocruntwice(17, True, True, {"iterations": 2022}, {"iterations": 1000000000000})
