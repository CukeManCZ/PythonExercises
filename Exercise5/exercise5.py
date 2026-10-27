x = [[0, 1], ['a', True], [1, 1.0, 2, 4]]

len(x)
type(x)

# Matice
x = []
for i in range(2):
   x.append([0] * 3)

# List methods
x.append()	    #Adds an element at the end of the list
x.clear()	    #Removes all the elements from the list
x.copy()	    #Returns a copy of the list
x.count()	    #Returns the number of elements with the specified value
x.extend()	    #Add the elements of a list (or any iterable), to the end of the current list
x.index()	    #Returns the index of the first element with the specified value
x.insert()	    #Adds an element at the specified position
x.pop()	        #Removes the element at the specified position
x.remove()	    #Removes the first item with the specified value
x.reverse()	    #Reverses the order of the list
x.sort()        #Sorts the list

#Unpacking
#print(*numbers, sep="-")

def printMatrix(matrix: list[list[float]]):
    for row in matrix:
        print(*row)

# Must be squared matrix
def matrixTrace(matrix: list[list[float]]):
    total = 0

    for i in range(len(matrix)):
        total += matrix[i][i]

    return total

# RN Rn*N
# vector is row [1,2,3] [[colum1], [colum2], [colum3]]
def multiVecMat(vector: list[float], matrix: list[list[float]]):
    if len(vector) != len(matrix):
        return None

    result = []

    for i in range(len(matrix[0])):     #Columns
        total = 0

        for j in range(len(matrix)):    #ROW
            total += vector[j] * matrix[j][i]

        result.append(total)

    return result

def allUnder(matrix: list[list[float]]) -> list[list[int]]:
    result = []

    for i in range(len(matrix)):            #ROW
        for j in range(len(matrix[i])):     #COLUMN
            if matrix[i][j] < 0:
                result.append([i, j])

    return result


def multiplyMat(A: list[list[float]], B: list[list[float]]):
    if len(A[0]) != len(B):
        return None

    result = []

    for i in range(len(A)):
        row = []

        for j in range(len(B[0])):
            total = 0

            for k in range(len(B)):
                total += A[i][k] * B[k][j]

            row.append(total)

        result.append(row)

    return result


x = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

print(matrixTrace(x))