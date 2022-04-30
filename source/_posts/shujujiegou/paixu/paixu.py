def bubble_sort(arr):
    """
    从小到大排序
    https://www.cnblogs.com/qlshine/p/6017957.html
    """
    l = len(arr)
    for i in range(l):
        for j in range(i, l): # 从小到大排序，每一轮最小的已经排到i的位置了
            if arr[j] < arr[i]:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
    return arr

arr = bubble_sort([5, 7, 1, 3, 10, 0.4])
print(arr)
