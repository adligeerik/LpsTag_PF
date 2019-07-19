import numpy as np
from scipy.optimize import minimize
from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def objective(x):
    distance = np.array([[0,1,1,sqrt(2)],[1,0,sqrt(2),1],[1,sqrt(2),0,1],[sqrt(2),1,1,0]])

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

    f01 = (x1-x0)**2+(y1-y0)**2+(z1-z0)**2-(distance[0][1]**2)
    f02 = (x2-x0)**2+(y2-y0)**2+(z2-z0)**2-(distance[0][2]**2)
    f03 = (x3-x0)**2+(y3-y0)**2+(z3-z0)**2-(distance[0][3]**2)

    f10 = (x0-x1)**2+(y0-y1)**2+(z0-z1)**2-(distance[1][0]**2)
    f12 = (x2-x1)**2+(y2-y1)**2+(z2-z1)**2-(distance[1][2]**2)
    f13 = (x3-x1)**2+(y3-y1)**2+(z3-z1)**2-(distance[1][3]**2)

    f20 = (x0-x2)**2+(y0-y2)**2+(z0-z2)**2-(distance[2][0]**2)
    f21 = (x1-x2)**2+(y1-y2)**2+(z1-z2)**2-(distance[2][1]**2)
    f23 = (x3-x2)**2+(y3-y2)**2+(z3-z2)**2-(distance[2][3]**2)

    f30 = (x0-x3)**2+(y0-y3)**2+(z0-z3)**2-(distance[3][0]**2)
    f31 = (x1-x3)**2+(y1-y3)**2+(z1-z3)**2-(distance[3][1]**2)
    f32 = (x2-x3)**2+(y2-y3)**2+(z2-z3)**2-(distance[3][2]**2)

    f = f01**2+f02**2+f03**2+f10**2+f12**2+f13**2+f20**2+f21**2+f23**2+f30**2+f31**2+f32**2
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
x0 = [0,0,0,1,0,0,0,1,0,1,1,0]

b = (-10,10)
bnds = (b,b,b,b,b,b,b,b,b,b,b,b)

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