# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/task/flags/
A non-empty zero-indexed array A consisting of N integers is given.

A peak is an array element which is larger than its neighbours. More precisely, it is an index P such that 0 < P < N − 1 and A[P − 1] < A[P] > A[P + 1].

For example, the following array A:

    A[0] = 1
    A[1] = 5
    A[2] = 3
    A[3] = 4
    A[4] = 3
    A[5] = 4
    A[6] = 1
    A[7] = 2
    A[8] = 3
    A[9] = 4
    A[10] = 6
    A[11] = 2
has exactly four peaks: elements 1, 3, 5 and 10.

You are going on a trip to a range of mountains whose relative heights are represented by array A, as shown in a figure below. You have to choose how many flags you should take with you. The goal is to set the maximum number of flags on the peaks, according to certain rules.



Flags can only be set on peaks. What's more, if you take K flags, then the distance between any two flags should be greater than or equal to K. The distance between indices P and Q is the absolute value |P − Q|.

For example, given the mountain range represented by array A, above, with N = 12, if you take:

two flags, you can set them on peaks 1 and 5;
three flags, you can set them on peaks 1, 5 and 10;
four flags, you can set only three flags, on peaks 1, 5 and 10.
You can therefore set a maximum of three flags in this case.

Write a function:

def solution(A)
that, given a non-empty zero-indexed array A of N integers, returns the maximum number of flags that can be set on the peaks of the array.

For example, the following array A:

    A[0] = 1
    A[1] = 5
    A[2] = 3
    A[3] = 4
    A[4] = 3
    A[5] = 4
    A[6] = 1
    A[7] = 2
    A[8] = 3
    A[9] = 4
    A[10] = 6
    A[11] = 2
the function should return 3, as explained above.

Assume that:

N is an integer within the range [1..400,000];
each element of array A is an integer within the range [0..1,000,000,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.

"""
def get_peaks(A):
    peaks = []
    L = len(A)
    for i in range(1, L - 1):
        pre = A[i - 1]
        cur = A[i]
        nex = A[i + 1]
        if cur > pre and cur > nex:
            peaks.append(i)
    return peaks


def get_peaks_len(peaks):
    return peaks[-1] - peaks[0]

def count_peaks(peaks, i):
    peaks_len = get_peaks_len(peaks)
    range_left = peaks_len
    last_peak = peaks[-1]
    flag_peak = None
    flags_left = i
    while i * (flags_left - 1) <= range_left:
        for peak in peaks:
            if flag_peak:
                range_left = last_peak - peak
                cur_dist = peak - flag_peak
            if flag_peak is None or cur_dist >= i:
                flags_left -= 1
                flag_peak = peak

            if flags_left == 0:
                break

        if flags_left == 0:
            return True
        return False

def solution(A):
    L = len(A)
    if L <= 2:
        return 0
    peaks = get_peaks(A)
    peaks_count = len(peaks)
    if peaks_count == 0:
        return 0
    elif peaks_count == 1:
        return 1
    for i in range(peaks_count, 0, -1):
        res = count_peaks(peaks, i)
        if res:
            return i
    return 0



#A = [1, 5, 3, 4, 3, 4, 1, 2, 3, 4, 6, 2]
A = [0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
#A = [0, 1, 0, 1, 0, 1]
#A = [1,1,1]
#A = [1,2, 1]
sol = solution(A)
print(sol)