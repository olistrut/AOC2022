exec(open("aochelper.py").read())

class Element:
    def __init__(self, name, op, operand1, operand2, number):
        self.name = name
        self.op = op
        self.operand1 = operand1
        self.operand2 = operand2
        self.humn = False
        self.result = number


def solveTree(root, elements):
    # recursive calc
    element = elements[root]
    if elements[root].op != None:
        op1 = solveTree(elements[root].operand1, elements)
        op2 = solveTree(elements[root].operand2, elements)
        result = int(eval(str(op1) + element.op + str(op2), {}, {}))
    else:
        result = elements[root].result
    elements[root].result = result
    return result


def labelHumnDep(root, elements):
    # recursively label all nodes dependent on the humn element
    if root == None: return False
    if elements[root].name == "humn":
        elements[root].humn = True
    else:
        elements[root].humn = labelHumnDep(elements[root].operand1, elements) or labelHumnDep(elements[root].operand2, elements)
    return elements[root].humn


def calcDown(root, goal, elements):
    # part 2 - ensure that the humn element of the tree is set to a value so that the whole humn-dependent side
    # eqals the other side

    # found our way to the bottom of the tree (to the humn element) - set to goal as calculated one level
    # further up
    if root == "humn":
        return goal

    # find which side is humn-dependent and which side can be calculated
    if elements[root].operand1!= None and elements[root].operand2 != None:
        if elements[elements[root].operand1].humn == True:
            humanEl = elements[root].operand1
            calcEl = elements[root].operand2
        elif elements[elements[root].operand2].humn == True:
            humanEl = elements[root].operand2
            calcEl = elements[root].operand1

    # calculate the side not dependent on the humn element
    subResult = solveTree(calcEl, elements)

    op = elements[root].op

    # recursively step into the humn-dependent side
    if root == "root":
        return calcDown(humanEl, subResult, elements)
    elif op == "+":
        return calcDown(humanEl, goal - subResult, elements)
    elif op == "*":
        return calcDown(humanEl, int(goal / subResult), elements)
    elif op == "-":
        if humanEl == elements[root].operand1:
            return calcDown(humanEl, goal + subResult, elements)
        else:
            return calcDown(humanEl, subResult - goal, elements)
    elif op == "/":
        if humanEl == elements[root].operand1:
            return calcDown(humanEl, goal * subResult, elements)
        else:
            return calcDown(humanEl, (subResult / goal), elements)


def solve(filename):
    result1 = 0
    result2 = 0

    file = open(filename)
    elements = {}

    while (s := file.readline().rstrip()):
        name, operation = s.split(": ")
        operation = operation.split(" ")
        if len(operation) == 1:
            # number only
            number = int(operation[0])
            e = Element(name, None, None, None, number)
        else:
            op1 = operation[0]
            op2 = operation[2]
            operand = operation[1]
            e = Element(name, operand, op1, op2, None)
            # print("Adding ", name, operand, op1, op2)
        elements[name] = e

    labelHumnDep("root", elements)
    result1 = solveTree("root", elements)
    result2 = calcDown("root", None, elements)

    elements["humn"].result = result2

    return result1, result2


########################
aocrunonce(21, True, True)
