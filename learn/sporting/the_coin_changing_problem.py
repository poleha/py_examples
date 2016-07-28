# -*- coding: utf-8 -*-
"""
https://codility.com/media/train/15-DynamicProgramming.pdf

For a given set of denominations, you are asked to find the minimum number of coins with
which a given amount of money can be paid. Assume that you can use as many coins of
a particular denomination as necessary. The greedy algorithmic approach is always to select
the largest denomination not exceeding the remaining amount of money to be paid. As long
as the remaining amount is greater than zero, the process is repeated. However, this algorithm
may return a suboptimal result. For instance, for an amount of 6 and coins of values 1, 3, 4,
we get 6 = 4 + 1 + 1, but the optimal solution here is 6 = 3 + 3.
A dynamic algorithm finds solutions to this problem for all amounts not exceeding the
given amount, and for increasing sets of denominations. For the example data, it would
consider all the amounts from 0 to 6, and the following sets of denominations: ∅, {1}, {1, 3}
and {1, 3, 4}. Let dp[i, j] be the minimum number of coins needed to pay the amount j if we
use the set containing the i smallest denominations. The number of coins needed must satisfy
the following rules:
• no coins are needed to pay a zero amount: dp[i, 0] = 0 (for all i);
• if there are no denominations and the amount is positive, there is no solution, so for
convenience the result can be infinite in this case: dp[0, j] = ∞ (for all j > 0);
• if the amount to be paid is smaller than the highest denomination ci
, this denomination
can be discarded: dp[i, j] = dp[i − 1, j] (for all i > 0 and all j such that ci > j);
• otherwise, we should consider two options and choose the one requiring fewer coins:
either we use a coin of the highest denomination, and a smaller amount to be paid
remains, or we don’t use coins of the highest denomination (and the denomination can
thus be discarded): dp[i, j] = min(dp[i, j − ci
] + 1, dp[i − 1, j]) (for all i > 0 and all j
such that ci ¬ j).
"""


#My, but based on their algorithm
#stud

MAX_INT = float('inf')

def dynamic_coin_changing(C, k):
    L = len(C)
    prev = [0] + [MAX_INT] * k
    for i in xrange(L):
        cur = []
        cur_max = C[i]
        for j in xrange(k + 1):
            if cur_max > j:
                cur.append(prev[j])
            else:
                cur.append(min(cur[j - cur_max] + 1, prev[j]))
        prev = cur
    return cur


C = [1, 3, 4]
k = 6

sol = dynamic_coin_changing(C, k)
print sol