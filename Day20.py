import collections

exec(open("aochelper.py").read())

class Element:
  def __init__(self, initialPos, number):
    self.number = number  # instance variable unique to each instance
    self.initialPos = initialPos
    self.pos = initialPos

  def __str__(self):
    return "Element: "+str(self.number)+" - initially at position: "+str(self.initialPos) + " - now at position: "+str(self.pos)

def move(elements, num):
  while elements[0].initialPos != num:
    elements.rotate(-1)

  storedElement = elements.popleft()

  rotationCount = storedElement.number % len(elements)

  elements.rotate(-rotationCount)
  elements.append(storedElement)

def solve(filename, **kwargs):
  multiplier = kwargs["multiplier"]
  rounds = kwargs["rounds"]

  result1 = 0

  file = open(filename)

  elements = collections.deque()

  pos = 0
  while (s:=file.readline().rstrip()):
    e = Element(pos, int(s)*multiplier)
    elements.append(e)
    pos += 1

  for round in range(rounds):
    #print("Round ", round)
    for i in range(pos):
      move(elements, i)

  # find 0 in list
  zeroPos = 0
  for e in elements:
    if e.number == 0:
      break
    zeroPos += 1

  result1 = elements[(zeroPos + 1000)%len(elements)].number + elements[(zeroPos + 2000)%len(elements)].number + elements[(zeroPos + 3000)%len(elements)].number
  return result1

#####################################################################################
aocruntwice(20, True, True, {"multiplier":1, "rounds":1}, {"multiplier":811589153, "rounds":10})
