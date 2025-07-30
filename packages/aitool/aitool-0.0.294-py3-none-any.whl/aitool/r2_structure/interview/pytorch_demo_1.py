# -*- coding: UTF-8 -*-
# @Time    : 2021/4/6
# @Author  : xiangyuejia@qq.com
# Apache License
# Copyright©2020-2021 xiangyuejia@qq.com All Rights Reserved
import torch

x = torch.Tensor(3, 5)
print(x)
y = torch.rand(3, 5)
print(y)
print(y.size())
y.add_(x)
print(y)