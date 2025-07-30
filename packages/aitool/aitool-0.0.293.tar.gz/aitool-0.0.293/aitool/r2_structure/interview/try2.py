# -*- coding: UTF-8 -*-
import sys


# dp[i][j] 用前i个单词填满j的长度 ， 0/1
# dp[i][j] = dp[i-i][j] or dp[i-1][j-len(w_i)]
# dp[0][len(w_0)] = 1


def solve(words, length):
    if len(words) == 0:
        return []
    dp = [[[] for _ in range(length + 1)] for _ in range(len(words))]
    dp[0][len(words[0])].append(0)
    max_length = len(words[0])
    ans = [0]
    print(dp)
    for i in range(1, len(words)):
        for j in range(1, length + 1):
            if len(dp[i - i][j]):
                dp[i][j] = dp[i - i][j]
            elif len(dp[i - 1][j - len(words[i])]):
                dp[i][j] = dp[i - 1][j - len(words[i])] + [i]
                print(i, j, dp[i][j])
                if j > max_length:
                    max_length = j
                    ans = dp[i][j]
    print(ans)
    out = [words[idx] for idx in ans]
    return out


if __name__ == '__main__':
    ws = ["apple", "banana", "cherry", "date", "elderberry", "fig"]
    # ws = ["a", "b"]

    print(solve(ws, 20))
