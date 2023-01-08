exec(open("aochelper.py").read())

def snafuToDecimal(s):
    decimal = 0
    for i in range(len(s)):
        power = len(s) - 1 - i
        c = s[i]
        if c == "-":
            c = -1
        elif c == "=":
            c = -2
        else:
            c = int(c)
        decimal += 5 ** power * c
    return decimal


def decimalToSnafu(decimal):
    snafu = ""
    carry = False
    while (True):
        r = decimal % 5
        decimal = int(decimal / 5)
        if carry:
            r += 1
        if r in [0, 1, 2]:
            snafu = str(r) + snafu
            carry = False
        elif r == 3:
            snafu = "=" + snafu
            carry = True
        elif r == 4:
            snafu = "-" + snafu
            carry = True
        elif r == 5:
            snafu = "0" + snafu
            carry = True
        if decimal == 0:
            if carry:
                snafu = "1" + snafu
            break

    return snafu


def solve(filename):
    file = open(filename)
    decimal = 0

    while (s := file.readline().rstrip()):
        decimal += snafuToDecimal(s)

    snafu = decimalToSnafu(decimal)
    decimal = snafuToDecimal(snafu)

    return snafu, decimal

############################
aocrunonce(25, True, True)

