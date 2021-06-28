alist = [4, 9, 1, 10]

def sort(alist):
    n = len(alist)
    for i in range(n):
        for j in range(0, n-i-1):
            if alist[j] < alist[j+1]:
                temp = alist[j]
                alist[j] = alist[j+1]
                alist[j+1] = temp
    return alist

print(sort(alist))

