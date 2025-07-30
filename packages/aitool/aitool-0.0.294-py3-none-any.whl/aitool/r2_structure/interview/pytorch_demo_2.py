# -*- coding: UTF-8 -*-
# @Time    : 2021/4/6
# @Author  : xiangyuejia@qq.com
# Apache License
# Copyright©2020-2021 xiangyuejia@qq.com All Rights Reserved

import torch
from torch.autograd import Variable
x = Variable(torch.ones(2, 2), requires_grad=True)
print(x)
y = x + 2
print(y)
print(y.grad_fn)
print(x.grad_fn)
z = y * y * 3
out = z.mean()
print(z, out)
out.backward()

from standard_search.core.standard_v3 import StandardV3
stan = StandardV3(synonyms_max_num=5)
print(stan.standardization("声带边有异物"))
