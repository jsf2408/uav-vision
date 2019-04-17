import numpy as np

def losslessResize(inputArray, outputSize):
    inputSize = inputArray.shape

    n = inputSize[1]/outputSize[1]
    m = inputSize[0]/outputSize[0]

    middleSize = (inputSize[0], outputSize[1])

    middleArray = np.empty(middleSize)
    values = []
    for i in range(0, middleSize[0]):
        for j in range(0, outputSize[1]):
            k = int(np.floor(n*j))
            while k < n*(j+1):
                values.append(inputArray[i,k])
                k = k+1
                middleArray[i,j] = max(values)
            values = []

    outputArray = np.empty(outputSize)

    values = []
    for j in range(0, outputSize[1]):
        for i in range(0, outputSize[0]):
            k = int(np.floor(m*i))
            while k < m*(i+1):
                values.append(middleArray[k,j])
                k = k+1
                outputArray[i,j] = max(values)
            values = []
    
    return outputArray

size1 = (4, 4) 
array = np.random.randint(100, size = size1)
print(array)
newSize = (4, 4)
newArray = losslessResize(array, newSize)
print(newArray)
