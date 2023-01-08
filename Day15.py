exec(open("aochelper.py").read())
import re

def solve(filename, **kwargs):
  size = kwargs["size"]
  rowToCount = kwargs["rowToCount"]

  result1 = 0
  result2 = 0
  xOffset = 0
  yOffset = 0
  #width = width+xOffset
  #height = height+yOffset


  file = open(filename)

  nonBeacon = {}
  beacons = {}
  sensors = {}
  sensorData = []

  count = 0
  while (line:=file.readline().rstrip()):
    coords = line.split("=")
    sensorX = int(coords[1].split(",")[0])
    sensorY = int(coords[2].split(":")[0])
    beaconX = int(coords[3].split(",")[0])
    beaconY = int(coords[4])
    sensors[(sensorY, sensorX)] = True
    beacons[(beaconY, beaconX)] = True

    distance = abs(sensorX - beaconX) + abs(sensorY - beaconY)
    sensorData.append((sensorY,sensorX, distance))

    if (sensorY <= rowToCount and sensorY + distance >= rowToCount) or (sensorY >= rowToCount and sensorY - distance <= rowToCount) :
      yDelta = abs(rowToCount - sensorY)
      for x in range(0,distance-yDelta+1):
        count += 1
        if not (rowToCount, sensorX+x) in beacons:
          nonBeacon[sensorX + x]=True
        if not (rowToCount, sensorX-x) in beacons:
          nonBeacon[sensorX - x]=True

  result1 = len(nonBeacon)

  for  (y, x, distance) in sensorData:
    distance += 1
    for yOffset in range(-distance,distance):
        xOffset = distance - yOffset
        if ((x + xOffset) < size) and ((y + yOffset) < size):
          covered = False
          for (y2, x2, distance2) in sensorData:
            if (abs(x+xOffset-x2)+abs(y+yOffset-y2)<=distance2):
              covered = True
              break
          if covered == False:
            result2 = (x+xOffset)*4000000+y+yOffset
            return result1, result2
        elif y+yOffset >= size:
          break

  return result1, result2

########################################################################################################
aocrunwithdataparams(15, True, True, {"rowToCount":10,"size":20}, {"rowToCount":2000000,"size":4000000})
