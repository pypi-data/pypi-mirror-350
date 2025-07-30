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
"""
from typing import Dict, Union, List, Any, NoReturn, Tuple


def get_batch(lst: List[Any], batch_size: int = 10) -> List[Any]:
    lst_len = len(lst)
    idx = 0
    while idx < lst_len:
        yield lst[idx: idx + batch_size]
        idx += batch_size
