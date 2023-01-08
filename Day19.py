exec(open("aochelper.py").read())

currentBest = (99,0)

def hypotheticalMax(rounds):
    # calculates the maximum number of geodes produced over n rounds if we build an additional geode robot each round
    result = int(rounds*(rounds+1)/2)
    return result

def dfs( maxRounds, blueprint, robots, inventory, minute, doNotBuild0, doNotBuild1, doNotBuild2):

  global currentBest

  newInventory = inventory.copy()
  # calculate output for the minute
  newInventory[0] += robots[0]
  newInventory[1] += robots[1]
  newInventory[2] += robots[2]
  newInventory[3] += robots[3]
  c = currentBest

  # see if we have a chance to catch up to the best observed state
  if minute < currentBest[0]:
      if (newInventory[3] + hypotheticalMax(currentBest[0]-minute+1) + robots[3]*(currentBest[0]-minute+1)) < currentBest[1]:
          # no chance of catching out -> exit
          return newInventory[3]
  if newInventory[3] > currentBest[1] and minute <= currentBest[0]:
      currentBest = (minute, newInventory[3])


  if minute == maxRounds:
    return newInventory[3]

  ###################
  obsidianThreshold = maxRounds-4
  if blueprint[3][2] > 10: obsidianThreshold = maxRounds-5
  if blueprint[3][2] > 15: obsidianThreshold = maxRounds-6
  if minute >= obsidianThreshold and robots[2] == 0:
    # we need at least 7 obsidian in each blueprint. with no obsidian robots in round 21, that is impossible
    return inventory[3]
    #, path

  # we need at least 7 clay for first obsidian robot (no later than round 22). without clay robot in round 19, that is impossible
  clayThreshold = obsidianThreshold - 4
  if blueprint[2][1] > 10: clayThreshold = obsidianThreshold - 5
  if blueprint[2][1] > 15: clayThreshold = obsidianThreshold - 6
  if minute >= clayThreshold and robots[1] == 0:
    return inventory[3]

  # make sure to maintain balance - not too many ore robots
  if minute >= 12 and robots[1]+2 < robots[0]: #+3
    return inventory[3]

  # there is no point hoarding ore and not building either ore or clay robots
  if minute > max(blueprint[0][0], blueprint[1][0])+1 and (robots[0] == 1) and (robots[1] == 0): #+2
    return inventory[3]



  result = 0
  if inventory[0] >= blueprint[3][0] and inventory[2] >= blueprint[3][2]:
        # enough ore to build geode robot
        #print("Minute ", minute, "building geode robot ", robots[3]+1, inventory)
        newInventory[0] -= blueprint[3][0]
        newInventory[2] -=  blueprint[3][2]
        robots[3] += 1
        #path.append((minute, "Geode Robot", robots, newInventory))
        #print(path)
        result = max(result, dfs( maxRounds, blueprint, robots, newInventory, minute +1, False, False, False))
          #retPath = p.copy()
        #path.pop()
        newInventory[0] +=  blueprint[3][0]
        newInventory[2] +=  blueprint[3][2]

        robots[3] -= 1

  else:
        if inventory[0] >= blueprint[2][0] and inventory[1] >= blueprint[2][1] and robots[2] < max(blueprint[0][2], blueprint[1][2], blueprint[2][2], blueprint[3][2]) and doNotBuild2 == False:

              newInventory[0] -= blueprint[2][0]
              newInventory[1] -= blueprint[2][1]
              robots[2] += 1
              #path.append((minute, "Obsidian Robot", robots.copy(), newInventory.copy()))
              result = max(result, dfs( maxRounds, blueprint, robots, newInventory,  minute +1, False, False, False))
                #retPath = p.copy()
              #path.pop()
              robots[2] -= 1
              newInventory[0] += blueprint[2][0]
              newInventory[1] += blueprint[2][1]

        if inventory[0] >= blueprint[1][0] and robots[1] < max(blueprint[0][1], blueprint[1][1], blueprint[2][1], blueprint[3][1])  and doNotBuild1 == False:
                # enough ore to build clay robot
                #print("Minute ", minute, "building clay robot ", robots[1]+1)

                newInventory[0] -= blueprint[1][0]#

                robots[1] += 1
                #path.append((minute, "Clay Robot", robots.copy(), newInventory.copy()))

                result = max(result,  dfs( maxRounds, blueprint, robots, newInventory, minute +1, False, False, False))
                  #retPath = p.copy()
                #path.pop()
                robots[1] -= 1
                newInventory[0] += blueprint[1][0]

        if inventory[0] >= blueprint[0][0] and robots[0] < max(blueprint[0][0], blueprint[1][0], blueprint[2][0], blueprint[3][0]) and doNotBuild0 == False:
                # enough ore to build ore robot
                newInventory[0] -= blueprint[0][0]
                robots[0] += 1
                #path.append((minute, "Ore Robot", robots.copy(), newInventory.copy()))

                result = max(result, dfs( maxRounds, blueprint, robots, newInventory, minute +1, False, False, False))
                  #retPath = p.copy()

                #path.pop()
                robots[0] -= 1
                newInventory[0] += blueprint[0][0]

        #path.append((minute, "No Op", robots.copy(), newInventory.copy()))
        doNotBuild0 = False
        doNotBuild1 = False
        doNotBuild2 = False
        if inventory[0] >= blueprint[0][0]:
                doNotBuild0 = True # skip this one in the next step if going for noop
        if inventory[0] >= blueprint[1][0]:
                doNotBuild1 = True
        if inventory[0] >= blueprint[2][0] and inventory[1] >= blueprint[2][1]:
                doNotBuild2 = True


        result = max(result, dfs( maxRounds, blueprint, robots, newInventory, minute + 1, doNotBuild0, doNotBuild1, doNotBuild2))
                #retPath = p.copy()
            #path.pop()

  return result
#, retPath



def solve(filename):
  result1 = 0
  result2 = 1
  global currentBest

  file = open(filename)
  num = 0
  r2 = 0

  while (s:=file.readline().rstrip()):
    num += 1
    blueprint = []
    input = s.split(" ")
    r1 = 0
    #print("Blueprint ", num)
    blueprint.append([int(input[6]),0,0])
    blueprint.append([int(input[12]),0,0])
    blueprint.append([int(input[18]), int(input[21]), 0])
    blueprint.append([int(input[27]), 0, int(input[30])])
    currentBest = (99, 0)

    r1  = dfs( 24, blueprint, [1,0,0,0], [0,0,0,0], 1, False, False, False)
    currentBest = (99, 0)

    if num in [1,2,3]:
       r2 = dfs( 32, blueprint, [1,0,0,0], [0,0,0,0], 1, False, False, False)
       result2 *= r2

    result1 += num * r1

  return result1, result2

###################################################################################
aocrunonce(19, True, True)
