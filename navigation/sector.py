import numpy as np

size1 = (600, 600) 
array = np.random.randint(256, size = size1)
print(array)

directions = ['l', 'r', 'u', 'd', 'c']
weight = [0] * 5

halfSize = [int(i / 2) for i in size1]

print(halfSize)

weight[0] = sum(sum(array[:, 0:halfSize[1]]))
weight[1] = sum(sum(array[:, halfSize[1]:]))
weight[2] = sum(sum(array[0: halfSize[0], :]))
weight[3] = sum(sum(array[halfSize[0]:, :]))

quarterSize = [i / (2*np.sqrt(2)) for i in size1]

weight[4] = sum(sum(array[int(halfSize[0]-quarterSize[0]):int(quarterSize[0]+halfSize[0]), int(halfSize[1]-quarterSize[1]):int(quarterSize[1]+halfSize[1])]))


print(weight)

direction = directions[weight.index(max(weight))]

print(direction)
