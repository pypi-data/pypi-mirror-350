# -*- coding: UTF-8 -*-
# Copyright xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Created on

3.无重复字符的最长子串
146.LRU缓存机制
206.反转链表
215.数组中的第K个最大..
25.K 个一组翻转链表
15.三数之和
53.最大子数组和
补充题4.手撕快速排序
21.合并两个有序链表
5.最长回文子串
102.二叉树的层序遍历
1.两数之和
33.搜索旋转排序数组
200.岛屿数量
46.全排列
121.买卖股票的最佳时机
88.合并两个有序数组
20.有效的括号
103.二叉树的锯齿形层次..
236.二叉树的最近公共祖先

"""
from tqdm import tqdm
from json import loads
from aitool import (timestamp, dump_excel, AutoPrompt, get_file, make_dir, get_doubao_img_base64, dump_pickle,
                    load_pickle, InputIdx, OutputIdx, LabelIdx, CommentIdx)
from random import sample, shuffle
from pandas import read_parquet
from collections import defaultdict
from PIL import Image
import io
from os import path
from tqdm import tqdm
import json
from aitool import dump_json, timestamp, dump_excel, load_excel, get_doubao_img_base64, infer_doubao_vision, load_pickle, dump_pickle, download_file
from aitool.r4_algorithm.llm.autoprompt.unit import AutoPrompt

def o1():
    make_data = True
    if make_data:
        all_data = []
        shuffle(all_data)
        data_test = []
        data_test_rst = []
        for line in all_data:
            idx0 = line[0]
            idx1 = line[1]
            idx2 = line[2]
            idx3 = line[3]
            pic_list = []
            for pic_path in idx2['pic_list']:
                if 'extract_path' not in pic_path:
                    continue
                if len(pic_list) >= 10:
                    continue
                pic_base64 = get_doubao_img_base64(pic_path)
                pic_list.append(pic_base64)
            idx2['pic_list'] = pic_list
            idx2['pic_type'] = 'base64'
            if len(pic_list) == 0:
                continue
            data_test.append((idx0, idx1, idx2, idx3))
            data_test_rst.append(idx0)
        dump_pickle(data_test, "./task4.5_local_all.pkl")
        dump_excel(data_test_rst, "./task4.5_local_all_rst.xlsx")

# 3
from collections import defaultdict
def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """
    if len(s) <= 1:
        return len(s)
    c2idx = [-1]*1000
    max_l = 0
    l = 0
    for tail in range(len(s)):
        l = l + 1
        head = tail - l + 1
        if c2idx[ord(s[tail])] >= head:
            l -= c2idx[ord(s[tail])] - head + 1
        max_l = max(max_l, l)
        c2idx[ord(s[tail])] = tail

    return max_l


if __name__ == '__main__':
    a = {1,2,3}
    a.pop()
    b = [1, 2, 3]
    b.pop()
    from collections import deque
    print(lengthOfLongestSubstring("bpfbhmipx"))
