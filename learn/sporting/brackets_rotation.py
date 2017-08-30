# -*- coding: utf-8 -*-
"""
A bracket sequence is considered to be a valid bracket expression if any of the following conditions is true:

it is empty;
it has the form "(U)" where U is a valid bracket sequence;
it has the form "VW" where V and W are valid bracket sequences.
For example, the sequence "(())()" is a valid bracket expression, but "((())(()" is not.

You are given a sequence of brackets S and you are allowed to rotate some of them. Bracket rotation means picking a single bracket and changing it into its opposite form (i.e. an opening bracket can be changed into a closing bracket and vice versa). The goal is to find the longest slice (contiguous substring) of S that forms a valid bracket sequence using at most K bracket rotations.

Write a function:

def solution(S, K)
that, given a string S consisting of N brackets and an integer K, returns the length of the maximum slice of S that can be transformed into a valid bracket sequence by performing at most K bracket rotations.

For example, given S = ")()()(" and K = 3, you can rotate the first and last brackets to get "(()())", which is a valid bracket sequence, so the function should return 6 (notice that you need to perform only two rotations in this instance, though).

Given S = ")))(((" and K = 2, you can rotate the second and fifth brackets to get ")()()(", which has a substring "()()" that is a valid bracket sequence, so the function should return 4.

Given S = ")))(((" and K = 0, you can't rotate any brackets, and since there is no valid bracket sequence with a positive length in string S, the function should return 0.

Assume that:

string S contains only brackets: '(' or ')';
N is an integer within the xrange [1..30,000];
K is an integer within the xrange [0..N].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N) (not counting the storage required for input arguments).
"""


from measure import measure
from collections import deque


xrange = range



# Correct but slow
def get_errors(S, L):
    errors = []
    open = deque()
    open_count = 0
    for i in xrange(L):
        cur = S[i]
        if cur == '(':
            open_count += 1
            open.append(i)
        else:
            if open_count == 0:
                errors.append(i)
            else:
                open_count -= 1
                open.pop()
    return errors + list(open)



def get_sum(errors, L):
    if not errors:
        return L
    stops = errors[:]
    max_s = 0
    prev_stop = None
    stop = None
    for stop in stops:
        if prev_stop is None:
            s = stop
        else:
            s = stop - prev_stop - 1
        max_s = max(s, max_s)
        prev_stop = stop
    if stop is not None and stop < L - 1:
        max_s = max(max_s, L - stop - 1)
    return max_s


def rotate(cur):
    if cur == '(':
        return ')'
    else:
        return '('

def get_change_points(S, L, errors):
    result = errors[:]
    if 0 not in errors:
        for i in xrange(errors[0]):
            cur = S[i]
            if cur == ')':
                result = [i] + result
                break
    if L - 1 not in errors:
        for i in xrange(L - 1, errors[-1], -1):
            cur = S[i]
            if cur == '(':
                result.append(i)
                break
    return result


@measure
def solution1(S, K):
    S = list(S)
    L = len(S)
    if L <= 1:
        return 0

    initial_errors = get_errors(S, L)
    if not initial_errors:
        return L
    max_len = get_sum(initial_errors, L)
    if K == 0:
        return max_len

    change_points = get_change_points(S, L, initial_errors)
    initial_errors = set(initial_errors)
    for i in xrange(len(change_points)):
        new_S = S[:]
        points = K
        left = None
        right = None
        for j in xrange(i, len(change_points)):
            change_point = change_points[j]
            prev_change_point = change_points[j - 1] if j - 1 >= 0 else None
            if left is None:
                left = new_S[change_point]
            elif right is None:
                right = new_S[change_point]
            if left and right:
                if left == right:
                    if prev_change_point not in initial_errors:
                        new_S[prev_change_point] = rotate(new_S[prev_change_point])
                    elif change_point not in initial_errors:
                        new_S[change_point] = rotate(new_S[change_point])
                    elif left == '(':
                        new_S[change_point] = rotate(new_S[change_point])
                    else:
                        new_S[prev_change_point] = rotate(new_S[prev_change_point])
                    points -= 1
                elif points >= 2:
                    new_S[prev_change_point] = rotate(new_S[prev_change_point])
                    new_S[change_point] = rotate(new_S[change_point])
                    points -= 2
                else:
                    break
                left = None
                right = None
                if points == 0:
                    break

        errors = get_errors(new_S, L)
        current_len = get_sum(errors, L)
        max_len = max(current_len, max_len)


    return max_len


#****************************************
@measure
def get_errors2(S, L):
    errors = []
    open = deque()
    open_count = 0
    for i in xrange(L):
        cur = S[i]
        if cur == '(':
            open_count += 1
            open.append(i)
        else:
            if open_count == 0:
                errors.append(i)
            else:
                open_count -= 1
                open.pop()
    return errors + list(open)


def get_sum2(errors, L):
    if not errors:
        return L
    max_s = 0
    prev_stop = None
    stop = None
    for stop in errors:
        if prev_stop is None:
            s = stop
        else:
            s = stop - prev_stop - 1
        max_s = max(s, max_s)
        prev_stop = stop
    if stop is not None and stop < L - 1:
        max_s = max(max_s, L - stop - 1)
    return max_s


def rotate2(cur):
    if cur == '(':
        return ')'
    else:
        return '('

def get_change_points2(S, L, errors):
    result = errors[:]
    if 0 not in errors:
        for i in xrange(errors[0]):
            cur = S[i]
            if cur == ')':
                result = [i] + result
                break
    if L - 1 not in errors:
        for i in xrange(L - 1, errors[-1], -1):
            cur = S[i]
            if cur == '(':
                result.append(i)
                break
    return result


@measure
def solution2(S, K):
    S = list(S)
    L = len(S)
    if L <= 1:
        return 0

    initial_errors = get_errors2(S, L)
    if not initial_errors:
        return L
    max_len = get_sum2(initial_errors, L)
    if K == 0:
        return max_len
    #additional_change_points = get_change_points2(S, L, initial_errors)
    change_points = get_change_points2(S, L, initial_errors)
    initial_errors = set(initial_errors)
    results = {}
    last_changed = None
    for i in xrange(len(change_points)):
        processed = False
        if i - 2 >= 0 and i - 2 in results:
            processed = True
            result = results[i - 2]
            try:
                new_error_left_index = change_points[i]
                new_error_right_index = change_points[i + 1]
            except:
                break
            try:
                new_error_left = S[new_error_left_index]
                new_error_right = S[new_error_right_index]
            except:
                break

            try:
                drop_error_left_index = change_points[result - 1]
                drop_error_right_index = change_points[result]
                drop_error_left = S[drop_error_left_index]
                drop_error_right = S[drop_error_right_index]
            except:
                break

            if drop_error_left != drop_error_right or new_error_left != new_error_right:
                processed = False
            elif new_error_left_index not in initial_errors or new_error_right not in initial_errors or drop_error_left_index not in initial_errors or drop_error_right_index not in initial_errors:
                processed = False
            else:
                end = change_points[i + 2] if i + 2 < len(change_points) else L
                current_len = end - drop_error_right_index - 1
                max_len = max(current_len, max_len)
                results[i] = new_error_right_index

                if end == L:
                    break

        if not processed:
            new_S = S[:]
            points = K
            left = None
            right = None
            for j in xrange(i, len(change_points)):
                change_point = change_points[j]
                prev_change_point = change_points[j - 1] if j - 1 >= 0 else None
                if left is None:
                    left = new_S[change_point]
                elif right is None:
                    right = new_S[change_point]
                if left and right:
                    if left == right:
                        if prev_change_point not in initial_errors:
                            new_S[prev_change_point] = rotate2(new_S[prev_change_point])
                        elif change_point not in initial_errors:
                            new_S[change_point] = rotate2(new_S[change_point])
                        elif left == '(':
                            new_S[change_point] = rotate2(new_S[change_point])
                        else:
                            new_S[prev_change_point] = rotate2(new_S[prev_change_point])
                        points -= 1
                    elif points >= 2:
                        new_S[prev_change_point] = rotate2(new_S[prev_change_point])
                        new_S[change_point] = rotate2(new_S[change_point])
                        points -= 2
                    else:
                        last_changed = j
                        break
                    left = None
                    right = None
                    if points == 0:
                        last_changed = j
                        break

            errors = get_errors2(new_S, L)
            current_len = get_sum2(errors, L)
            max_len = max(current_len, max_len)

            results[i] = last_changed

    return max_len


#************************************
def get_errors3(S, L):
    errors = []
    open = deque()
    open_count = 0
    for i in xrange(L):
        cur = S[i]
        if cur == '(':
            open_count += 1
            open.append(i)
        else:
            if open_count == 0:
                errors.append(i)
            else:
                open_count -= 1
                open.pop()
    return errors + list(open)

def get_change_points3(S, L, errors):
    result = errors[:]
    i = None
    j = None
    left_additional_error_index = right_additional_error_index = None
    if 0 not in errors:
        for i in xrange(errors[0]):
            cur = S[i]
            if cur == ')':
                result = [i] + result
                break
    if L - 1 not in errors:
        for j in xrange(L - 1, errors[-1], -1):
            cur = S[j]
            if cur == '(':
                result.append(j)
                break

    if i:
        for k in xrange(i):
            cur = S[k]
            if cur == '(':
                left_additional_error_index = k

    if j:
        for k in xrange(L - 1, j, -1):
            cur = S[k]
            if cur == ')':
                right_additional_error_index = k

    return result, left_additional_error_index, right_additional_error_index

def get_sum3(errors, L):
    if not errors:
        return L
    max_s = 0
    prev_stop = None
    stop = None
    for stop in errors:
        if prev_stop is None:
            s = stop
        else:
            s = stop - prev_stop - 1
        max_s = max(s, max_s)
        prev_stop = stop
    if stop is not None and stop < L - 1:
        max_s = max(max_s, L - stop - 1)
    return max_s

def get_special_error_index(S, errors):
    prev_error = None
    for i in xrange(len(errors)):
        error = errors[i]
        if prev_error is not None:
            real_prev_error = S[prev_error]
            real_error = S[error]
            if real_prev_error != real_error:
                return i - 1
        prev_error = error
    return None


# Осталось понять. Если справа осталась одна ошибка, то надо пытаться вертеть следующее за ней. Также слева. Если одна ошибка
#


@measure
def _solution3(S, K):
    S = list(S)
    L = len(S)
    if L <= 1:
        return 0

    initial_errors = get_errors3(S, L)

    special_error_index = get_special_error_index(S, initial_errors)

    if not initial_errors:
        return L
    max_len = get_sum3(initial_errors, L)
    if K == 0:
        return max_len
    errors = initial_errors
    #errors, left_additional_error_index, right_additional_error_index = get_change_points3(S, L, initial_errors)
    errors_len = len(errors)
    for i in xrange(errors_len):
        start_error_index = errors[i]
        if special_error_index is not None:
            left_len = special_error_index - i - 1
        else:
            left_len = None
        special_error_inside = False
        # Get last fixed error
        fixed_errors_count = None
        end_error_index0 = i + K * 2 - 1
        if end_error_index0 >= errors_len:
            end_error_index0 = errors_len - 1
            fixed_errors_count = end_error_index0 - i + 1
            if fixed_errors_count % 2 == 1:
                # Если исправили нечетное количество ошибок, последняя ошибка вылетает.
                end_error_index0 -= 1

        if special_error_index is not None and i <= special_error_index < end_error_index0 and special_error_index + 1 <= end_error_index0 and left_len and left_len % 2 == 1:
            special_error_inside = True

        if fixed_errors_count is not None:
            points_left = K - fixed_errors_count / 2
        else:
            points_left = 0

        if special_error_inside and points_left < 1:
                end_error_index0 -= 2

        if end_error_index0 <= i:
            continue

        #end_error_index = errors[end_error_index0]

        # Get next error
        try:
            next_error_index0 = end_error_index0 + 1
            next_error_index = errors[next_error_index0]
        except:
            next_error_index = None


        #Get start
        if i == 0:
            start = 0
        else:
            prev_error_index = errors[i - 1]
            start = prev_error_index + 1

        # get length
        if next_error_index is not None:
            end = next_error_index
        else:
            end = L

        s = end - start
        max_len = max(s, max_len)


    return max_len


@measure
def solution3(S, K):
    S1 = list(S)
    S2 = list(S)
    L = len(S)
    for i in xrange(L):
        cur = S[i]
        if cur == ')':
            S1[i] = '('
            break
    for i in xrange(L - 1, -1, -1):
        cur = S[i]
        if cur == '(':
            S2[i] = ')'
            break
    sol1 = _solution3(S1, K - 1)
    sol2 = _solution3(S2, K - 1)
    sol = _solution3(S, K)
    return max(sol, sol1, sol2)



#**********************************************


def get_errors4(S, L, fixes=None):
    fixes = fixes if fixes else {}
    errors = []
    open = deque()
    open_count = 0
    for i in xrange(L):
        cur = fixes.get(i) or S[i]
        if cur == '(':
            open_count += 1
            open.append(i)
        else:
            if open_count == 0:
                errors.append(i)
            else:
                open_count -= 1
                open.pop()
    return errors + list(open)



def get_sum4(errors, L):
    if not errors:
        return L
    stops = errors[:]
    max_s = 0
    prev_stop = None
    stop = None
    for stop in stops:
        if prev_stop is None:
            s = stop
        else:
            s = stop - prev_stop - 1
        max_s = max(s, max_s)
        prev_stop = stop
    if stop is not None and stop < L - 1:
        max_s = max(max_s, L - stop - 1)
    return max_s


def rotate4(cur):
    if cur == '(':
        return ')'
    else:
        return '('

def get_change_points4(S, L, errors):
    result = errors[:]
    if 0 not in errors:
        for i in xrange(errors[0]):
            cur = S[i]
            if cur == ')':
                result = [i] + result
                break
    if L - 1 not in errors:
        for i in xrange(L - 1, errors[-1], -1):
            cur = S[i]
            if cur == '(':
                result.append(i)
                break
    return result


@measure
def solution4(S, K):
    S = list(S)
    L = len(S)
    if L <= 1:
        return 0

    initial_errors = get_errors4(S, L)
    if not initial_errors:
        return L
    max_len = get_sum4(initial_errors, L)
    if K == 0:
        return max_len

    change_points = get_change_points4(S, L, initial_errors)
    initial_errors = set(initial_errors)
    for i in xrange(len(change_points)):
        fixes = {} # Stores positions of fixes from original list
        сurrent_test_len = 0
        points = K
        left = None
        right = None
        for j in xrange(i, len(change_points)):
            change_point = change_points[j]
            prev_change_point = change_points[j - 1] if j - 1 >= 0 else None
            if left is None:
                left = S[change_point]
            elif right is None:
                right = S[change_point]
            if left and right:
                if left == right:
                    if prev_change_point not in initial_errors:
                        fixes[prev_change_point] = rotate(S[prev_change_point])
                        start = max(prev_change_point - 1, 0)
                    elif change_point not in initial_errors:
                        fixes[change_point] = rotate4(S[change_point])
                        end = min(change_point + 1, L - 1)
                    elif left == '(':
                        fixes[change_point] = rotate4(S[change_point])
                        start = change_points[i]
                    else:
                        fixes[prev_change_point] = rotate4(S[prev_change_point])

                    points -= 1
                    fixed = True
                elif points >= 2:
                    fixes[prev_change_point] = rotate4(S[prev_change_point])
                    fixes[change_point] = rotate4(S[change_point])
                    points -= 2
                    fixed = True
                else:
                    fixed = False
                    break
                if fixed:
                    if left not in initial_errors and left in fixes:
                        start = change_points[i]
                    else:
                        start = change_points[i] if i - 1 in initial_errors else 0
                    if right not in initial_errors and right in fixes:
                        end = change_points[j]
                    else:
                        end = change_points[j + 1] if j < len(change_points) - 1 else L

                    сurrent_test_len = end - start

                left = None
                right = None
                if points == 0:
                    break


        errors = get_errors4(S, L, fixes=fixes)
        current_len = get_sum4(errors, L)
        max_len = max(сurrent_test_len, max_len)

    return max_len


"""
Идея в том, что нам нужно не менять исходный массив, а хранить места, которые мы изменили. - done
И по "вылеченным" местам определять, какова длина правильного участка.
То есть нам нужна первая ошибка или начало и последняя ошибка или конец.
"""



S = '())'
K = 2
#S = '))(('



sol1 = solution1(S, K)

sol4 = solution4(S, K)
#S = list(reversed(S))
#sol3 = max(solution3(S, K), sol3)

print(sol1, sol4)

"""
import random

variants = ['(', ')']


for k in xrange(10000):
    l = random.choice(list(xrange(1, 8)))
    K = random.choice(list(xrange(1, 8)))

    S = ''
    for i in xrange(l):
        variant = random.choice(variants)
        S += variant
    sol1 = solution1(S, K)
    #sol2 = solution2(S, K)
    #sol3 = solution3(S, K)
    sol4 = solution4(S, K)
    if sol1 != sol4:
        print('S=', S, 'K=', K, 'sol1=',  sol1, 'sol4=', sol4)


print(measure.timers)
"""