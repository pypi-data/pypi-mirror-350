# -*- coding: UTF-8 -*-
# 快速排序
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = []
        right = []
        for num in arr[1:]:
            if num <= pivot:
                left.append(num)
            else:
                right.append(num)
        return quick_sort(left) + [pivot] + quick_sort(right)


def quick_sort_in_place(arr, low, high):
    if low < high:
        # 分区操作，获取基准元素的最终位置
        pivot_index = partition(arr, low, high)
        # 递归排序基准元素左边的子数组
        quick_sort_in_place(arr, low, pivot_index - 1)
        # 递归排序基准元素右边的子数组
        quick_sort_in_place(arr, pivot_index + 1, high)


def partition(arr, low, high):
    # 选择最后一个元素作为基准元素
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            # 交换元素
            arr[i], arr[j] = arr[j], arr[i]
    # 将基准元素放到正确的位置
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# 堆排序
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


# 测试代码
arr = [3, 6, 8, 10, 1, 2, 1]
print("快速排序结果:", quick_sort(arr))
print("堆排序结果:", heap_sort(arr.copy()))
print(quick_sort_in_place(arr, 0, len(arr)-1))
