exec(open("aochelper.py").read())

import functools
import ast

def compare(left, right):
  if type(left) == int and type(right) == int:
      return left - right
  elif type(left) == int:
      left = [left]
  elif (type(right) == int):
      right = [right]

  # Comparing 2 lists
  for i in range(min(len(left), len(right))):
     # call recursively
     r = compare(left[i], right[i])
     if (r != 0):
       return r

  return len(left)-len(right)


def solve(filename):
  result1 = 0
  result2 = 0

  lists = []

  file = open(filename)

  pairNum = 1

  blocks = file.read().split("\n\n")

  for block in blocks:
    left, right = map(ast.literal_eval, block.split())
    lists.append(left)
    lists.append(right)

    if compare(left, right) < 0:
      result1 += pairNum

    pairNum +=1

  lists.append([[2]])
  lists.append([[6]])

  lists.sort(key=functools.cmp_to_key(compare))
  result2 = (lists.index([[2]]) +1) * (lists.index([[6]])+1)

  return result1, result2


######################################################################################
aocrunonce(13, True, True)





