# Need pyeda
from pyeda.inter import *
import collections.abc
collections.Sequence = collections.abc.Sequence

#generating a boolean expression for a given integer and node
def generateBoolExpression(i, node):
    varFormat = "{:05d}".format(int(bin(i)[2:]))
    expression = ""

    for index in range(5):
        if index != 0:
            expression += "&"

        if varFormat[index] == '0':
            expression += "~"
        
        expression += f"{node}[{index}]"

    return expression

#creating a BDD expression
def createBDDexpression(values, node):
    expression = ""

    for i in values:
        if expression != "":
            expression += "|"
        
        expression += f"({generateBoolExpression(i, node)})"
    
    return expr(expression)


def generateRR():

    expression = ""

    for i in range(32):
        for j in range(32):
            if ((i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32):
                if expression != "":
                    expression += "|"
                
                expression += f"(({generateBoolExpression(i, 'x')}) & ({generateBoolExpression(j, 'y')}))"

    return expr(expression)


def computeTwoStep(r1, r2):

    r1 = r1.compose({
        y[0]: z[0], y[1]: z[1], y[2]: z[2], y[3]: z[3], y[4]: z[4]
    })

    r2 = r2.compose({
        x[0]: z[0], x[1]: z[1], x[2]: z[2], x[3]: z[3], x[4]: z[4]
    })
    return r1 & r2


def computeRR2star(r):

    RR2star = r
    while True:
        prev = RR2star
        RR2star = prev | computeTwoStep(RR2star, r)
        if RR2star.equivalent(prev):
            break
    return RR2star


def convertNumToDict(num, node):

    result = {}
    str = "{:05d}".format(int(bin(num)[2:]))
    for i in range(5):
        result[node[i]] = int(str[i])
    return result


# Step 3.1 Functions

# if the RR holds between num 1 and num 2
def checkRR(num1, num2):

    v1 = convertNumToDict(num1, x)
    v2 = convertNumToDict(num2, y)
    v1.update(v2)

    return bool(RRbdd.restrict(v1))

#if the number is even
def checkEven(num):

    val = convertNumToDict(num, y)

    return bool(Ebdd.restrict(val))

#if the number is prime
def checkPrime(num):

    val = convertNumToDict(num, x)

    return bool(Pbdd.restrict(val))


# step 3.2 Functions

#if the RR2 between num 1 and num 2
def checkRR2(num1, num2):

    v1 = convertNumToDict(num1, x)
    v2 = convertNumToDict(num2, y)
    v1.update(v2)

    return bool(RR2bdd.restrict(v1))

# if the RR2Star between num 1 and num 2
def checkRRstar(num1, num2):

    v1 = convertNumToDict(num1, x)
    v2 = convertNumToDict(num2, y)
    v1.update(v2)

    return bool(RR2starbdd.restrict(v1))


# Test Cases

def testRR():
    #RR(27, 3) - TRUE
    print("RR(27, 3): " + str(checkRR(27, 3)))
    
    #RR(16, 20) - FALSE
    print("RR(16, 20): " + str(checkRR(16, 20)))


def testEven():
    #EVEN(14) - TRUE
    print("EVEN(14): " + str(checkEven(14)))
    
    #EVEN(13) - FALSE
    print("EVEN(13): " + str(checkEven(13)))


def testPrime():
    #PRIME(7) - TRUE
    print("PRIME(7): " + str(checkPrime(7)))
    
    #PRIME(2) - FALSE
    print("PRIME(2): " + str(checkPrime(2)))


def testRR2():
    #RR2(27, 6) - TRUE
    print("RR2(27, 6): " + str(checkRR2(27, 6)))
    
    #RR2(27, 9) - FALSE
    print("RR2(27, 9): " + str(checkRR2(27, 9)))


def testStatementA():
    not_exists_u = Pbdd & ~Ebdd.smoothing(y)
    result = ~not_exists_u
    return result.is_one()


if __name__ == '__main__':
    
    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 5)

    # prime and even 
    prime = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    even = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

    # creating BDDs
    RRbdd = expr2bdd(generateRR())
    Pbdd = expr2bdd(createBDDexpression(prime, 'x'))
    Ebdd = expr2bdd(createBDDexpression(even, 'y'))

    # Compute RR2 and RR2star 
    RR2bdd = computeTwoStep(RRbdd, RRbdd)
    RR2bdd.smoothing(z)
    RR2starbdd = computeRR2star(RRbdd)

    #print test cases and output
    print("\nStep 3.1 ---------------------\n")
    testRR()
    testEven()
    testPrime()

    print("\nStep 3.2 ---------------------\n")
    testRR2()

    print("\nStep 3.4 ---------------------\n\nStatement A is ", "True" if testStatementA() else "False")
