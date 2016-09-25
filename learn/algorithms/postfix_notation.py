from collections import deque
from string import digits, ascii_uppercase

# http://aliev.me/runestone/BasicDS/InfixPrefixandPostfixExpressions.html
# stud
def infixToPostfix(infixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = deque()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in digits + ascii_uppercase:
            postfixList.append(token)
        elif token == '(':
            opStack.append(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while opStack and prec[opStack[-1]] >= prec[token]:
                postfixList.append(opStack.pop())

            opStack.append(token)

    while opStack:
        postfixList.append(opStack.pop())
    return " ".join(postfixList)





#print(infixToPostfix("A * B + C * D"))
#print(infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )"))
#print(infixToPostfix("A * B + C"))
#print(infixToPostfix("A + B * C"))
#print(infixToPostfix("( A + B )  * C"))



def postfixEval(postfixExpr):
    operands = deque()
    expr = postfixExpr.split()


    for token in expr:
        try:
            token = int(token)
            is_operand = True
        except:
            is_operand = False

        if is_operand:
            operands.append(token)
        else:
            right = operands.pop()
            left = operands.pop()
            res = eval("{}{}{}".format(left, token, right))
            operands.append(res)
    return operands[0]

#print(postfixEval('7 8 + 3 2 + /'))
#print(postfixEval('17 10 + 3 * 9 /'))


A = infixToPostfix("5 * 3 ^ ( 4 - 2 )")
print(A)
print(postfixEval(A))