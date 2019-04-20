import numpy as np

size1 = (10, 10) 
array = np.zeros(size1)
array[:, 4:5] = 50/10
#array[:, 0] = 200/200
#array[:, 9] = 200
print(array)

centre = [0] * 2
mass = sum(sum(array))
print(mass)

tune = [1, 1]

massX = sum(array)
print(massX)
print(massX.shape[0])
for i in range(0,massX.shape[0]):
    distance = (i/((massX.shape[0]-1)/2))-1
    if distance == 0:
        continue
    if distance < 0:
        massX[i] = -massX[i]*(tune[0]*abs(1/distance)+(1-tune[0]))
    elif distance > 0:
        massX[i] = massX[i]*(tune[0]*(1/distance)+(1-tune[0]))
print(massX)
print(sum(massX))
centre[0] = (sum(massX)/mass)#+1)*(massX.shape[0]/2)

##massY = sum(np.rot90(np.fliplr(array)))
##for i in range(0,massY.shape[0]):
##    massY[i] = massY[i]*(i+1)
##centre[1] = sum(massY)/mass-1

print(centre)

