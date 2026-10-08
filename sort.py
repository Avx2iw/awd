import random
Data_Set = []
for _ in range(1,10) :
    Data_Set.append(random.randint(1,10))
print(Data_Set)

class sorts() :
    #bubble sort
    
    def Bubble_Sort(set) :
        for i in range(len(set)) :
            for j in range(0, len(set) - i - 1) :
                if set[j] > set[(j + 1)] :
                    set[j], set[(j + 1)] = set[(j + 1)], set[j]
        print(set)

    #insertion sort
    
    def insertion_sort(set):
        for i in range(1, len(set)):
            key = set[i]
            j = i - 1
            while j >= 0 and set[j] > key:
                set[j + 1] = set[j]
                j = j - 1
            set[j + 1] = key
sorts.insertion_sort(Data_Set)
print(Data_Set)