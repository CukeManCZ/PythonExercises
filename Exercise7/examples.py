
#Stack (zásobník)
s = []
s.append("A")    # push
s.append("B")
s.append("C")    # s = ["A", "B", "C"]
print(s.pop())   # "C"  (poslední vložený)
print(s[-1])     # "B"  (nahlédnutí na vrch bez odebrání)
print(len(s) == 0)  # test prázdnosti


#Queue (fronta)
from collections import deque

q = deque()
q.append("A")      # enqueue (na konec)
q.append("B")
q.append("C")
print(q.popleft()) # "A"  (první vložený)
print(q[0])        # "B"  (nahlédnutí na začátek)
print(len(q) == 0)