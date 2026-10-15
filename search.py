#TESTING
import random
dataset = []
for i in range(0,10):
    dataset.append(random.randint(1,10))
print(dataset)
target = 5
#TESTING

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
        global lower
        global upper
        lower = 0
        upper = len(array) - 1
        while lower <= upper:
            mid = (upper + lower) // 2
            if array[mid] < target:
                lower = mid + 1
            elif array[mid] > target:
                upper = mid - 1
            else:
                return mid
        return -1

#TESTING
print(search.binary(dataset, target))
#TESTING