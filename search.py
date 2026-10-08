#TESTING
import random
dataset = []
for i in range(1,10):
    dataset.append(random.randint(1,10))
print(dataset)
target = 5
#TESTING

class search() :

    #Linear search
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
        print(*pos, sep=",")
        print(count)
                



#TESTING
search.linear(dataset, target)
#TESTING