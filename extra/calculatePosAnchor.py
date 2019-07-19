import numpy as np
from scipy.optimize import minimize
from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def objective(x):
    distance = np.array([[0,1,1,sqrt(2),sqrt(3)],[1,0,sqrt(2),1,sqrt(2)],[1,sqrt(2),0,1,sqrt(2)],[sqrt(2),1,1,0,1],[sqrt(3),sqrt(2),sqrt(2),1,0]])
    
    noise = np.array([[1.35865414e-02, 2.03503872e-02, 5.68674466e-02, 6.66487760e-02,
        6.44043707e-02],
       [2.44540611e-02, 3.83970580e-02, 5.10788547e-02, 5.17023643e-02,
        6.79218521e-05],
       [2.50795239e-02, 9.64046466e-02, 5.97754551e-03, 3.10001477e-02,
        7.45819149e-02],
       [7.17065492e-02, 8.07143201e-02, 4.97779901e-02, 2.41304877e-02,
        8.09613238e-02],
       [6.74279918e-02, 6.36712012e-02, 2.18220883e-02, 1.72943754e-02,
        9.92220512e-02]])


    distance = distance + noise

    x0 = x[0]
    y0 = x[1]
    z0 = x[2]
    
    x1 = x[3]
    y1 = x[4]
    z1 = x[5]
    
    x2 = x[6]
    y2 = x[7]
    z2 = x[8]
    
    x3 = x[9]
    y3 = x[10]
    z3 = x[11]

    x4 = x[12]
    y4 = x[13]
    z4 = x[14]

    f01 = ((x1-x0)**2+(y1-y0)**2+(z1-z0)**2-(distance[0][1]**2))**2
    f02 = ((x2-x0)**2+(y2-y0)**2+(z2-z0)**2-(distance[0][2]**2))**2
    f03 = ((x3-x0)**2+(y3-y0)**2+(z3-z0)**2-(distance[0][3]**2))**2
    f04 = ((x4-x0)**2+(y4-y0)**2+(z4-z0)**2-(distance[0][4]**2))**2

    f10 = ((x0-x1)**2+(y0-y1)**2+(z0-z1)**2-(distance[1][0]**2))**2
    f12 = ((x2-x1)**2+(y2-y1)**2+(z2-z1)**2-(distance[1][2]**2))**2
    f13 = ((x3-x1)**2+(y3-y1)**2+(z3-z1)**2-(distance[1][3]**2))**2
    f14 = ((x4-x1)**2+(y4-y1)**2+(z4-z1)**2-(distance[1][4]**2))**2

    f20 = ((x0-x2)**2+(y0-y2)**2+(z0-z2)**2-(distance[2][0]**2))**2
    f21 = ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2-(distance[2][1]**2))**2
    f23 = ((x3-x2)**2+(y3-y2)**2+(z3-z2)**2-(distance[2][3]**2))**2
    f24 = ((x4-x2)**2+(y4-y2)**2+(z4-z2)**2-(distance[2][4]**2))**2

    f30 = ((x0-x3)**2+(y0-y3)**2+(z0-z3)**2-(distance[3][0]**2))**2
    f31 = ((x1-x3)**2+(y1-y3)**2+(z1-z3)**2-(distance[3][1]**2))**2
    f32 = ((x2-x3)**2+(y2-y3)**2+(z2-z3)**2-(distance[3][2]**2))**2
    f34 = ((x4-x3)**2+(y4-y3)**2+(z4-z3)**2-(distance[3][4]**2))**2

    f40 = ((x0-x4)**2+(y0-y4)**2+(z0-z4)**2-(distance[4][0]**2))**2
    f41 = ((x1-x4)**2+(y1-y4)**2+(z1-z4)**2-(distance[4][1]**2))**2
    f42 = ((x2-x4)**2+(y2-y4)**2+(z2-z4)**2-(distance[4][2]**2))**2
    f43 = ((x3-x4)**2+(y3-y4)**2+(z3-z4)**2-(distance[4][3]**2))**2

    f = \
    f01+f02+f03+f04+\
    f10+f12+f13+f14+\
    f20+f21+f23+f24+\
    f30+f31+f32+f34+\
    f40+f41+f42+f43

    return f

def constrain1(x):
    return x[0]

def constrain2(x):
    return x[1]

def constrain3(x):
    return x[2]

def constrain4(x):
    return x[3] - 1 

def constrain5(x):
    return x[4] 

def constrain6(x):
    return x[5] 

def distance(x0,x1):
    return(sqrt((x1[0]-x0[0])**2+(x1[1]-x0[1])**2+(x1[2]-z0[2])**2))

#def main():
x0 = [0,0,0,1,0,0,0,1,0,1,1,0,1,1,1]

b = (-10,10)
bnds = (b,b,b,b,b,b,b,b,b,b,b   ,b,b,b,b)

const1 = {'type':'eq','fun':constrain1}
const2 = {'type':'eq','fun':constrain2}
const3 = {'type':'eq','fun':constrain3}
const4 = {'type':'eq','fun':constrain4}
const5 = {'type':'eq','fun':constrain5}
const6 = {'type':'eq','fun':constrain6}

cons = [const1,const2,const3,const4,const5,const6]

sol = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons)

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


#main()