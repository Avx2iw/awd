
class search() :
    #|Linear search|
    def linear(array, target):
        global count
        global pos
        pos = []
        count = 0
        for j in range(len(array)):
            if array[j] == target:
                j = j + 1
                count = count + 1
                pos.append(j)
            elif j == len(array):
                return
        if pos == []:
            pos.append('None')
        return ("target = " + str(target) + "\npositions = " + str(pos) + "\ncount = " + str(count))
    
    #|Binary search|
    def binary(array, target):
        arraysorted = sorted(array)
        global lower
        global upper
        global count
        global k
        lower = 0
        upper = len(arraysorted) - 1
        count = arraysorted.count(target)
        k = 0
        pos = []
        while k < count:
            while lower <= upper:
                mid = (upper + lower) // 2
                if arraysorted[mid] < target:
                    lower = mid + 1
                elif arraysorted[mid] > target:
                    upper = mid - 1
                else:
                    pos.append(mid)
                    k = k + 1
                    upper = mid - 1
        return ("sorted array = " + str(arraysorted) + "\npositions = " + str(pos) + "\ncount = " + str(count))
