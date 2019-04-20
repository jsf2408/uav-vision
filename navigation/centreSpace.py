import numpy as np

size1 = (10000, 10000) 
array = np.random.randint(256, size = size1)
print(array)

centre = [0] * 2
mass = sum(sum(array))
print(mass)

massX = sum(array)
for i in range(0,massX.shape[0]):
    massX[i] = massX[i]*(i+1)
centre[0] = sum(massX)/mass-1

massY = sum(np.rot90(np.fliplr(array)))
for i in range(0,massY.shape[0]):
    massY[i] = massY[i]*(i+1)
centre[1] = sum(massY)/mass-1

print(centre)

