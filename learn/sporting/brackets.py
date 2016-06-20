# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/brackets/
A string S consisting of N characters is considered to be properly nested if any of the following conditions is true:

S is empty;
S has the form "(U)" or "[U]" or "{U}" where U is a properly nested string;
S has the form "VW" where V and W are properly nested strings.
For example, the string "{[()()]}" is properly nested but "([)()]" is not.

Write a function:

def solution(S)
that, given a string S consisting of N characters, returns 1 if S is properly nested and 0 otherwise.

For example, given S = "{[()()]}", the function should return 1 and given S = "([)()]", the function should return 0, as explained above.

Assume that:

N is an integer within the range [0..200,000];
string S consists only of the following characters: "(", "{", "[", "]", "}" and/or ")".
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N) (not counting the storage required for input arguments).
"""

def is_opposite(left, right):
    if left == '{' and right == '}' or \
       left == '(' and right == ')' or \
       left == '[' and right == ']':
        return True
    else:
        return False

def is_left(s):
    if s in ['{', '(', '[']:
        return True
    return False


def solution(S):
    L = len(S)
    lefts = []
    for i in range(L):
        cur = S[i]
        if is_left(cur):
            lefts.append(cur)
        elif lefts:
            left = lefts.pop()
            if not is_opposite(left, cur):
                return 0
        else:
            return 0
    if not lefts:
        return 1
    else:
        return 0




#S = "{[()()]}"
#S = "([)()]"
S = ")"
sol = solution(S)
print(sol)

