exec(open("aochelper.py").read())
import re
import math

class Monkey:
  def __init__(self, id):
    self.id = id
    self.items = None
    self.operation = None
    self.op1 = None
    self.op2 = None
    self.divisor = None
    self.targetIfTrue = None
    self.targetIfFalse = None

def solve(filename, **kwargs):
  rounds = kwargs["rounds"]
  divideBy = kwargs["divideBy"]
  result1 = 0

  inspected=[]

  file = open(filename)
  monkey = None
  monkeys = {}
  modulo = 1

  while (s:=file.readline()):
    s = s.rstrip()
    match = re.search('Monkey (\d+):', s)
    n = 0
    if match:
      num = int(match.group(1))
      monkey = Monkey(num)
      monkeys[num] = monkey
      inspected.append(0)

    match = re.search('  Starting items: (.*)', s)
    if match:
        curItems = [int(item) for item in match.group(1).split(",")]
        monkey.items = curItems

    match = re.search('Test: divisible by (\d+)', s)
    if match:
      divisor = int(match.group(1))
      modulo = modulo * divisor
      monkey.divisor = divisor

    match = re.search("Operation: new = (.*) ([\+\*]) (.*)", s)
    if match:
      op = match.group(2)
      monkey.operation = op
      monkey.op1 = match.group(1)
      monkey.op2 = match.group(3)
    match = re.search("    If true: throw to monkey (\d+)", s)
    if match:
      monkey.targetIfTrue = int(match.group(1))
    match = re.search("    If false: throw to monkey (\d+)", s)
    if match:
      monkey.targetIfFalse = int(match.group(1))

  # play
  for round in range(rounds):
    for num, m in monkeys.items():
      for i in range(len(monkeys[num].items)):
        item = m.items.pop(0)

        op = m.operation
        op1 = m.op1
        op2 = m.op2
        #print("  Inspecting item with level ",item)
        inspected[int(num)]+=1
        if (op1 == "old"):
          op1 = item
        else:
          op1 = int(op1)
        if (op2 == "old"):
          op2 = item
        else:
          op2 = int(op2)
        if (op=="*"):
             item = (op1 * op2) % modulo
        elif(op=="+"):
          item = (op1 + op2) %modulo

        item = int(item/divideBy)

        target = -1
        if (item % monkeys[num].divisor == 0):
          #item = 0
          target = monkeys[num].targetIfTrue
        else:
          target = monkeys[num].targetIfFalse

        monkeys[target].items.append(item)
        # print("  Throwing ", item," from ", num," to ", target)

  inspected = sorted(inspected, reverse = True)
  result1 = inspected[0] * inspected[1]
  return result1


######################################################################################
aocruntwice(11, True, True,{"rounds":20, "divideBy":3}, {"rounds":10000, "divideBy":1})



