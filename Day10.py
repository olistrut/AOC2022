exec(open("aochelper.py").read())


def clockCheck(clock, value):
    if (clock == 20 or clock == 60 or clock == 100 or clock == 140 or clock == 180 or clock == 220):
        return clock * value
    else:
        return 0


def renderPixel(clock, value):
    render = ""
    # clock starts at 1, screen pos at 0 - alternatively could change if below to >= clock -1 and <= clock
    clock -= 1
    clock = clock % 40

    if (value in [clock - 1, clock, clock + 1]):
        render += "#"
    else:
        render += "."

    if (clock == 39):
        render += '\n'
    return render


def solve(filename, **kwargs):
    result1 = 0
    result2 = "\n"
    clock = 1
    cmd = inc = ""
    xReg = 1
    file = open(filename)

    while (s := file.readline().rstrip()):
        result1 += clockCheck(clock, xReg)
        result2 += renderPixel(clock, xReg)

        if (s != "noop"):
            cmd, inc = s.split(" ")
            clock += 1

            result1 += clockCheck(clock, xReg)
            result2 += renderPixel(clock, xReg)
            xReg += int(inc)

        else:
            cmd = "noop"

        clock += 1

    return result1, result2


#########################
aocrunonce(10, True, True)
