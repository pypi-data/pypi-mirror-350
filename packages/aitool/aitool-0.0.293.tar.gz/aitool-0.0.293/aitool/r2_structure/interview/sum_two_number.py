# -*- coding: UTF-8 -*-
# @Time    : 2021/4/6
# @Author  : xiangyuejia@qq.com
# Apache License
# Copyright©2020-2021 xiangyuejia@qq.com All Rights Reserved
from typing import List


def x(numbers: List[int], target: int) -> List[int]:
    len_of_numbers = len(numbers)
    for i in range(len_of_numbers):
        for j in range(i+1, len_of_numbers):
            if numbers[i] + numbers[j] == target:
                return [numbers[i], numbers[j]]


if __name__ == '__main__':
    n = [1, 2, 3, 4, 5]
    t = 7
    print(x(n, t))
