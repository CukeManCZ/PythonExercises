import copy
a = [0] * 5
 
#shallow deep copy
b = a
c = a[:]
d = list(a)
 
a[3] = 3
b[0] = -5
c[4] = 4

c = copy.deepcopy(a)

#print(a)
#print(b)
#print(c)
#print(d)

#List rows
f = []
for i in range(3):
    f.append([i] * 3)

g = [[i] * 3 for i in range(3)]

#print([1]*3)

print(f)
print(g)


        
