import numpy as np
from scipy.optimize import minimize
from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#distance = np.array([[0,1,1,sqrt(2),sqrt(3)],
#                    [1,0,sqrt(2),1,sqrt(2)],
#                    [1,sqrt(2),0,1,sqrt(2)],
#                    [sqrt(2),1,1,0,1],
#                    [sqrt(3),sqrt(2),sqrt(2),1,0]])

#distance = np.array([[0,1,1,sqrt(2)],
#                    [1,0,sqrt(2),1],
#                    [1,sqrt(2),0,1],
#                    [sqrt(2),1,1,0]])

#orginal
#distance = np.array([[0,4.395,5.248,6.321],
#                    [4.378,0,3.522,5.229],
#                    [5.244,3.538,0,1.651],
#                    [6.286,5.233,1.675,0]])

#distance = np.array([[0,4.395,5.248,6.321],
#                    [4.395,0,3.538,5.229],
#                    [5.248,3.538,0,1.675],
#                    [6.321,5.229,1.675,0]])

#distance = np.array([[0,438,524,630],
#                    [438,0,353,523],
#                    [524,353,0,166],
#                    [630,523,166,0]])


distance = np.array([[0,4.400,5.200,6.000],
                     [4.400,0,3.000,5.000],
                     [5.200,3.000,0,1.000],
                     [6.000,5.000,1.000,0]])

#noise = np.array([[1.35865414e-02, 2.03503872e-02, 5.68674466e-02, 6.66487760e-02,6.44043707e-02],
#    [2.44540611e-02, 3.83970580e-02, 5.10788547e-02, 5.17023643e-02,6.79218521e-05],
#    [2.50795239e-02, 9.64046466e-02, 5.97754551e-03, 3.10001477e-02,7.45819149e-02],
#    [7.17065492e-02, 8.07143201e-02, 4.97779901e-02, 2.41304877e-02,8.09613238e-02],
#    [6.74279918e-02, 6.36712012e-02, 2.18220883e-02, 1.72943754e-02,9.92220512e-02]])
#
#distance = distance + noise

numNodes = len(distance)

def objective(coordinates,distance):

    numCord = len(coordinates)

    x = []
    y = []
    z = []
    for i in range(0,numCord,3):
        x.append(coordinates[i])
        y.append(coordinates[i+1])
        z.append(coordinates[i+2])

    numNodes = numCord/3
    f = 0
    for i in range(numNodes):
        for j in range(numNodes):
            if j == i:
                continue
            f = f + ((x[j]-x[i])**2+(y[j]-y[i])**2+(z[j]-z[i])**2-(distance[i][j]**2))**2 

    return f

def constrain1(x):
    return x[0]

def constrain2(x):
    return x[1]

def constrain3(x):
    return x[2]

def constrain4(x):
    return x[3] - distance[0][1] 

def constrain5(x):
    return x[4] 

def constrain6(x):
    return x[5]

#def constrain7(x):
#    return x[8] 

def distanceCal(x0,x1):
    return(sqrt((x1[0]-x0[0])**2+(x1[1]-x0[1])**2+(x1[2]-z0[2])**2))


x0 = [0] * (numNodes*3)
xstart = [0,0,0,distance[0][1],0,0]
b = (-10000000,1000000)
bounds = []
for i in range(len(xstart)):
    x0[i] = xstart[i]

for i in range(numNodes*3):
    bounds.append(b)

bnds = tuple(bounds)

const1 = {'type':'eq','fun':constrain1}
const2 = {'type':'eq','fun':constrain2}
const3 = {'type':'eq','fun':constrain3}
const4 = {'type':'eq','fun':constrain4}
const5 = {'type':'eq','fun':constrain5}
const6 = {'type':'eq','fun':constrain6}
#const7 = {'type':'eq','fun':constrain6}

cons = [const1,const2,const3,const4,const5,const6]

sol = minimize(objective,x0,args=distance,method='SLSQP',bounds=bnds,constraints=cons)

print(sol)
xcoor = []
ycoor = []
zcoor = []

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(0,len(sol.x),3):
    xcoor.append(sol.x[i])
    ycoor.append(sol.x[i+1])
    zcoor.append(sol.x[i+2])
    ax.scatter(sol.x[i],sol.x[i+1],sol.x[i+2])
plt.show()
