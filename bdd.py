from pyeda.inter import *
import collections.abc
collections.Sequence = collections.abc.Sequence



def createExpression(i, node):

    var_format = "{:05d}".format(int(bin(i)[2:]))
    var_expression = ""

    for index in range(5):
        if index != 0:
            var_expression += "&"
        
        if var_format[index] == '0':
            var_expression += "~"
        
        var_expression += f"{node}[{index}]"

    return var_expression


def createBDD(values, node):
    BDDExprssion = None
    expression = ""

    for i in values:
        if expression != "":
            expression += "|"
        
        expression += f"({createExpression(i, node)})"
    
    return expr(expression)

def createRR():
    expression = ""

    for i in range(32):
        for j in range(32):
            if ((i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32):
                if expression != "":
                    expression += "|"
                
                expression += f"(({createExpression(i, 'x')}) & ({createExpression(j, 'y')}))"

    return expr(expression)

def compute2Step(RR1, RR2):

    RR1 = RR1.compose({y[0]:z[0], y[1]:z[1], y[2]:z[2], y[3]:z[3], y[4]:z[4]})
    RR2 = RR2.compose({x[0]:z[0], x[1]:z[1], x[2]:z[2], x[3]:z[3], x[4]:z[4]})
    return RR1 & RR2

def computeRR2Star(RR):

    RR2Star = RR
    while (1):
        RR2StarPrime = RR2Star
        RR2Star = RR2StarPrime | compute2Step(RR2Star, RR)
        if (RR2Star.equivalent(RR2StarPrime)):
            break
    return RR2Star


def numToDictionary(num, node):

    result = {}
    num = ("%05d" % int(bin(num)[2:]))
    for i in range(5):
        result[node[i]] = int(num[i])
    return result

# FUNCTIONS -----------------------------------

# For step 3.1
def RR(num1, num2):

    val1 = numToDictionary(num1, x)
    val2 = numToDictionary(num2, y)
    val1.update(val2)
    return bool(RR_BDD.restrict(val1))

def EVEN(num):
    val = numToDictionary(num, y)
    return bool(E.restrict(val))

def PRIME(num):
    val = numToDictionary(num, x)
    return bool(P.restrict(val))

# For step 3.2
def RR2(num1, num2):

    val1 = numToDictionary(num1, x)
    val2 = numToDictionary(num2, y)
    val1.update(val2)
    return bool(RR2_BDD.restrict(val1))
    
def RR2Star(num1, num2):
    val1 = numToDictionary(num1, x)
    val2 = numToDictionary(num2, y)
    val1.update(val2)
    return bool(RR2Star_BDD.restrict(val1))




# TEST CASES ------------------------------------------------

# Fpr step 3.1
def test_RR():
    
    #RR(27, 3) - TRUE
    print("RR(27,3): " + str(RR(27, 3)))

    #RR(16, 20) - FALSE
    print("RR(16, 20): " + str(RR(16, 20)))

def test_EVEN():

    #EVEN(14) - TRUE
    print("EVEN(14): " + str(EVEN(14)))

    #EVEN(13) - FALSE
    print("EVEN(13): " + str(EVEN(13)))

def test_PRIME():
    #PRIME(7) - TRUE
    print("PRIME(7): " + str(PRIME(7)))

    #PRIME(2) - FALSE
    print("PRIME(2): " + str(PRIME(2)))


# For step 3.2

def test_RR2():
    #RR2(27, 6) - TRUE
    print("RR2(27, 6): " + str(RR2(27, 6)))

    #RR2(27, 9) - FALSE
    print("RR2(27, 9): " + str(RR2(27, 9)))

 

def testStatementA():
    notExisits_u = P & ~E.smoothing(y)
    result = ~notExisits_u

    return result.is_one()

if __name__ == '__main__':

    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 5)

    prime = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    even = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

    RR_BDD = expr2bdd(createRR())

    
    P = expr2bdd(createBDD(prime, 'x'))
    E = expr2bdd(createBDD(even, 'y'))

    RR2_BDD = compute2Step(RR_BDD, RR_BDD)
    RR2_BDD.smoothing(z)
    RR2Star_BDD = computeRR2Star(RR_BDD)

    # Test cases
    print("\nStep 3.1 ---------------------\n")
    test_RR()
    
    test_EVEN()
    
    test_PRIME()

    print("\nStep 3.2 ---------------------\n")
    test_RR2()

    #Last Step
    print("\nStep 3.4 ---------------------\n\nStatement A is ", "True" if testStatementA() else "False")
