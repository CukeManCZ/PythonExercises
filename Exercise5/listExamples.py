def my_find(a, b):
    if len(b) == 0:
        return 0

    for i in range(len(a) - len(b) + 1):
        if a[i:i + len(b)] == b:
            return i

    return -1

def my_replace(a, b, c):
    if len(b) == 0:
        return a

    vysledek = []
    i = 0

    while i < len(a):
        if a[i:i + len(b)] == b:
            vysledek += c
            i += len(b)
        else:
            vysledek += [a[i]]
            i += 1

    return vysledek

def word_change():
    while True:
        a = input()

        a = a.replace("Ahoj", "Cau")
        print(a)

        if "Konec" in a:
            break


inputList = [0, 5, 3, 6, 20]
cut = inputList[-3:]
print(cut)

findSequence = [6, 20]
replaceSequence = [1]

print(my_replace(inputList, findSequence, replaceSequence))

#Sorting
result = [x for x in inputList if x > 10]
8 in result       # True
100 in result     # False
8 not in result   # False
sorted(inputList, reverse=True)

def distance_from_10(n):
    return abs(n - 10)  # Return a number used for comparison
sorted(inputList, key=distance_from_10)
#sequence[start:stop:step]


#Enum examples ---------------------------------------------
from enum import Enum
class PlantState(Enum):
    NONE = 1
    PLANTED = 2
    GROWING_1 = 3
    GROWING_2 = 4
    GROWING_3 = 5
    FINISHED = 6

x = PlantState.NONE
print(x)


