# -*- coding: UTF-8 -*-

def sr(a, b, e):
    if e - b <= 0:
        return
    k = a[b]
    i = b
    j = e
    while i < j:
        while i < j and a[j] >= k:
            j -= 1
        a[i] = a[j]
        while i < j and a[i] <= k:
            i += 1
        a[j] = a[i]
    a[i] = k
    sr(a, b, i-1)
    sr(a, i+1, e)


def solve(a):
    sr(a, 0, len(a)-1)


ts = [15, 13, 10, 3, 6, 9, 1, 7, 14, 2, 8, 5, 5, 4, 11, 12]
solve(ts)
print(ts)
