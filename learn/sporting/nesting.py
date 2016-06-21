# -*- coding: utf-8 -*-
"""
A string S consisting of N characters is called properly nested if:

S is empty;
S has the form "(U)" where U is a properly nested string;
S has the form "VW" where V and W are properly nested strings.
For example, string "(()(())())" is properly nested but string "())" isn't.

Write a function:

def solution(S)
that, given a string S consisting of N characters, returns 1 if string S is properly nested and 0 otherwise.

For example, given S = "(()(())())", the function should return 1 and given S = "())", the function should return 0, as explained above.

Assume that:

N is an integer within the range [0..1,000,000];
string S consists only of the characters "(" and/or ")".
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(1) (not counting the storage required for input arguments).
"""

# O(N)
def solution(S):
    L = len(S)
    if L % 2 != 0:
        return 0
    lefts_count = 0
    for cur in S:
        if cur == '(':
            lefts_count += 1
        else:
            lefts_count -= 1
        if lefts_count < 0:
            return 0
    if lefts_count > 1:
        return 0
    return 1

l = '(' * 1000
r = ')' * 1000
S = l + r

sol = solution(S)
print(sol)