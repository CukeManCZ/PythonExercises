output = "testValue"

def getList(ourList : list[float], separator : str = "|") -> str:
    output = "<"
    for value in ourList:
        output += f"{value}{separator}"
    output += ">"
    return (output, 5, 6)

"""
def max(values : list[float]) -> float:
maxCurrent = values[0]
for x in values:
if x > maxCurrent:
maxCurrent = x
return maxCurrent
"""

# (10) -> 10 + 9 + 8 + 7 + .... + 1
def getSum(value : int) -> int:
    if value == 1:
        return 1

    return value + getSum(value - 1)

def readProducts():
    product = {}
    with open("Exercise4/product.txt", "r") as stream:
        for line in stream:
            productLine = line.split()
            name = productLine[0]
            count = int(productLine[1])
            value = float(productLine[2])

            product[name] = (count, value)

    return product

def writeProducts(products):
    with open("Exercise4/product.txt", "w") as stream:
        for name in products:
            outputLine = f"{name} {products[name][0]} {products[name][1]}\n"
            stream.write(outputLine)

def addProduct(products, product):
    name, count, value = product
    products[name] = (count, value)
    return products

def removeProduct(products, productName):
    del products[productName]
    return products

def getProductsValues(products):
    productValue = 0
    for name in products:
        productValue += products[name][0] * products[name][1]
    return productValue


products = readProducts()
while True:
    name = input("Enter product to remove:")
    removeProduct(products, name)
    writeProducts(products)

    print(getProductsValues(products))