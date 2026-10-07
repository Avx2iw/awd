import random
Data_Set = []
for _ in range(1,10) :
    Data_Set.append(random.randint(1,10))
print(Data_Set)

#bubble sort
class sorts() :
    def Bubble_Sort(set) :
        for i in range(len(set)) :
            for j in range(0, len(set) - i - 1) :
                if set[j] > set[(j + 1)] :
                    set[j], set[(j + 1)] = set[(j + 1)], set[j]
        print(set)

sorts.Bubble_Sort(Data_Set)
