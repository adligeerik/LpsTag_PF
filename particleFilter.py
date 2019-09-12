import math
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
from random import uniform, gauss
import numpy as np
import time
from collections import OrderedDict
import copy


'''{"id":"0x4909","ts":"160253.5610","msgid":3767147,"usb":0,"acc":"[10.27,0.891,0.364]","gyro":"[0.2,0.3,-1.2]","mag":[122,127,215],"ref_anchor":"5b3","meas":[{"addr":"5b3","ddist":"-0.051","tqf":1,"rssi":"-79.0"},{"addr":"4a30","ddist":"1.126","tqf":1,"rssi":"-78.5"},{"addr":"611","ddist":"-1.725","tqf":1,"rssi":"-78.9"}]}'''


def calculateDdist(particle, anchorMap):
    # Distance to the ref_anchor (ref_ancor is in 0,0,0 by definition)

    ddistDict = {}
    refAnchorDist = math.sqrt(particle[0]**2 + particle[1]**2 + particle[2]**2)

    # Calculate the ddist to all other anchors. ddist is the difference in lenght from the ref_anchor to another anchor.
    for anchor in anchorMap:
        # Coordinate for that anchor (landmark)
        pos = anchorMap[anchor]

        if pos['ref_anchor'] == 1:
            ddistDict[anchor] = 0
            continue

        # Euclidean distance differnece from with regards to the ref_anchor
        ddist = math.sqrt((pos['x']-particle[0])**2 + (pos['y']-particle[1])**2 + (pos['z']-particle[2])**2)
        ddist = ddist - refAnchorDist
        ddistDict[anchor] = ddist
    
    return ddistDict


''' Move particles 
Move particle according to the integral of acceleration
time between latest measurment and the one before that.
Dist to move = acceleration * time
'''
def moveParticles(particles,acceleration,timestamp):

    # Time difference between this and last measurment
    timestep = 0 # timestamp - lastts

    # Acceleration in for this measurment
    #ax = acceleration[0]
    #ay = acceleration[1]
    #az = acceleration[2]

    ax = gauss(0,1.0)/10
    ay = gauss(0,1.0)/10
    az = gauss(0,1.0)/10

    # Distance to move all particles
    dx = ax*timestep
    dy = ay*timestep
    dz = az*timestep

    # Variance of the accelerometers measurement
    varAcc = 1

    for particle in particles:
        particle[0] = particle[0] + dx + gauss(0,varAcc)/15
        particle[1] = particle[1] + dy + gauss(0,varAcc)/15
        particle[2] = particle[2] + dz + gauss(0,varAcc)/15


''' Update map in particles'''
def updateMap(particles):
    return 0


''' Normalize weight 
Calculates the sum of all weights and normalize the weight for all particles'''
def normalizeWeight(particles):

    weightSum = 0
    # Sumation of all weights
    for particle in particles:
        weightSum = particle[3] + weightSum

    # Normalization of the weights
    for particle in particles:
        particle[3] = particle[3] / weightSum



''' Assign Weight '''
def assignWeight(particles,anchorMap,measurement):
    
    anchorOrder = []
    mean = []
    for anchor in measurement:
        anchorOrder.append(anchor["addr"])
        mean.append(anchor["ddist"])

    # Needs to be calculated before (or updated during)
    # !!!!!!!! NEEDS TO BE CHANGED !!!!!!!!
    variance = 0.02
    n = len(anchorOrder)
    cov = [] 

    for i in range(len(anchorOrder)):
        var = [0]*n
        var[i]= variance
        cov.append(var)
    # !!!!!!!! NEEDS TO BE CHANGED !!!!!!!!
    highP = 0
    for particle in particles:
        ddist = []
        ddistval = calculateDdist(particle,anchorMap)
        for anchor in anchorOrder:
            ddist.append(ddistval[anchor])
        
        
        mean = map(float,mean)
        #Calculates the probability of that particle
        p = multivariate_normal.pdf(ddist, mean, cov)
        particle[3] = p
        if p > highP:
            highP = p
    #print("highest p: " + str(highP))
    return highP

''' Init
m - number of particles
'''
def init(numParticles,map,minmax):
    particles = []
    
    # Search for the refernace anchor
    for anchor in map:
        if map[anchor]["ref_anchor"] == 1:
            refAnchor = anchor 
            

    # Init uniform random position for all particles
    for i in range(0,numParticles):
        x = uniform(minmax['maxx'], minmax['minx'])
        y = uniform(minmax['maxy'], minmax['miny'])
        z = uniform(minmax['maxz'], minmax['minz'])

        # Create a particle
        try:
            particle = [x,y,z,0]
        except UnboundLocalError:
            print(UnboundLocalError)
            print("\n Problaby no ref_anchor in map \n")

        # Add particle
        particles.append(particle)

    return particles


''' Low variance sampling '''
def lowVarianceSampling(particles):

    newParticles = []

    M = len(particles)
    r = uniform(0,1.0/M)
    inM = 1.0/M
    c = particles[0][3]
    i = 0
    for m in range(M):
        U = r + m*inM
        while( U > c ):
            i = i + 1
            c = c + particles[i][3]
        newParticles.append([particles[i][0],particles[i][1],particles[i][2],particles[i][3]])

    return(newParticles)


''' Chooses the particle with the highest weight
'''
def highestWeight(particles):
    bestWeight = 0
    mu = {}
    for particle in particles:
        if particle.weight > bestWeight:
            bestWeight = particle.weight
            mu["x"] = particle.x
            mu["y"] = particle.y
            mu["z"] = particle.z

    return mu

''' Calulcates the mean coordinate of all particles
'''
def meanPos(particles):
    mu = {}
    mu["x"] = 0
    mu["y"] = 0
    mu["z"] = 0
    for particle in particles:
        mu["x"] = particle[0] + mu["x"]
        mu["y"] = particle[1] + mu["y"]
        mu["z"] = particle[2] + mu["z"]

    M = len(particles)

    mu["x"] = mu["x"]/M
    mu["y"] = mu["y"]/M
    mu["z"] = mu["z"]/M

    return mu

''' Weighted average'''
def weightedAverage(particles):

    mu = {}
    mu["x"] = 0
    mu["y"] = 0
    mu["z"] = 0
    for particle in particles:
        mu["x"] = particle[0]*particle[3] + mu["x"]
        mu["y"] = particle[1]*particle[3] + mu["y"]
        mu["z"] = particle[2]*particle[3] + mu["z"]

    M = len(particles)

    mu["x"] = mu["x"]/M
    mu["y"] = mu["y"]/M
    mu["z"] = mu["z"]/M
    return mu

''' Most likely position
The most likely position of the tag given all the particles'''
def bestPos(particles):
    #mu = highestWeight(particles)
    mu = meanPos(particles)
    #mu = weightedAverage(particles)
    return mu

''' Particle filter '''
def particleFilter(particles,anchorMap,dataPackage):

    try:
        measurement = dataPackage["meas"]

        # Converts string list to float list
        acceleration = dataPackage["acc"]
        acceleration = acceleration.replace('"','')
        acceleration = acceleration.replace('[','')
        acceleration = acceleration.replace(']','')
        acceleration = acceleration.split(',')
        acceleration = map(float, acceleration)
    except KeyError:
        print(KeyError)
        mu = bestPos(particles)
        return (particles, mu,None)
    timestep = dataPackage["ts"]

    # Calculate weight
    pHigh = assignWeight(particles,anchorMap,measurement)

    # Normalize weight
    normalizeWeight(particles)

    # Resample
    particles = lowVarianceSampling(particles)
    
    # Move particles
    moveParticles(particles,acceleration,timestep)    

    # Gives a extimated position from the particles
    mu = bestPos(particles)

    return (particles, mu, pHigh)


''' Main
map - coordinates for landmarks
'''
def main():

    # Read map
    mapfile = open("extra/coordinates.json","r")
    mapstr = mapfile.read()
    anchorMap = json.loads(mapstr)


    # Number of particles 
    numParticles = 100

    # Between what coordinates the particles should be initialized 
    xAnchor = []
    yAnchor = []
    zAnchor = []
    for anchor in anchorMap:
        xAnchor.append(anchorMap[anchor]["x"])
        yAnchor.append(anchorMap[anchor]["y"])
        zAnchor.append(anchorMap[anchor]["z"])

    # 1.2 is arbitrary choosen to have some particles outside of the anchors
    minmax = {
    "maxx":max(xAnchor)*1.2,
    "minx":min(xAnchor)*1.2,
    "maxy":max(yAnchor)*1.2,
    "miny":min(yAnchor)*1.2,
    "maxz":max(zAnchor)*1.2+1,
    "minz":min(zAnchor)*1.2-1.5,
    }

    # Init particles
    particles = init(numParticles, anchorMap, minmax)
    
    # Visualisation
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    diff = [max(xAnchor) - min(xAnchor), max(yAnchor) - min(yAnchor), max(zAnchor) - min(zAnchor)]

    if diff.index(max(diff)) == 0:
        span = (diff[0]/2)*1.2

    if diff.index(max(diff)) == 1:
        span = (diff[1]/2)*1.2

    if diff.index(max(diff)) == 2:
        span = (diff[2]/2)*1.2

    xmean = np.mean(xAnchor)
    ymean = np.mean(yAnchor)
    zmean = np.mean(zAnchor)

    # Set limit for axes 
    ax.set_xlim3d(xmean-span,xmean+span)
    ax.set_ylim3d(ymean-span,ymean+span)
    ax.set_zlim3d(zmean-span,zmean+span)

    # Read file with tag data for simulation
    tagdata = open("extra/batmovetagdataall.json","r")

    coord = [[],[],[]]
    variance = [[],[],[]]
    pHigh = []

    for index,line in enumerate(tagdata):
        
        print("index: "+str(index))
        ax.clear()
        ax.set_xlim3d(xmean-span,xmean+span)
        ax.set_ylim3d(ymean-span,ymean+span)
        ax.set_zlim3d(zmean-span,zmean+span)

        try:
            dataPackage = json.loads(line)
        except ValueError:
            print(ValueError)
            continue
        
        # Draw anchors
        for i, anchor in enumerate(anchorMap):
            ax.scatter(anchorMap[anchor]["x"],anchorMap[anchor]["y"],anchorMap[anchor]["z"], c='blue')
            ax.text(anchorMap[anchor]["x"],anchorMap[anchor]["y"],anchorMap[anchor]["z"], anchor)
        
        # Call the particle filter
        (particles,mu,pHighest) = particleFilter(particles,anchorMap,dataPackage)
        
        # Display the particles
        npParticle = np.array(particles).transpose()
        ax.plot(npParticle[0],npParticle[1],npParticle[2],'.', c='red')

        xpos = []
        ypos = []
        zpos = []
        for particle in particles:
            xpos.append(particle[0])
            ypos.append(particle[1])
            zpos.append(particle[2])
        xvar = np.var(xpos)
        yvar = np.var(ypos)
        zvar = np.var(zpos)

        print("Variance, x: "+str(xvar)+", y: "+str(yvar)+", z: "+str(zvar))

        ax.scatter(mu["x"],mu["y"],mu["z"], c='green')

        coord[0].append(mu["x"])
        coord[1].append(mu["y"])
        coord[2].append(mu["z"])

        variance[0].append(xvar)
        variance[1].append(yvar)
        variance[2].append(zvar)

        pHigh.append(pHighest)
        print("highest p: " + str(pHighest))

        fig.canvas.draw()
        fig.canvas.flush_events()

        if index > 4000:
            break

    tagdata.close()

    ax.set_xlim3d(xmean-span,xmean+span)
    ax.set_ylim3d(ymean-span,ymean+span)
    ax.set_zlim3d(zmean-span,zmean+span)

    for i, anchor in enumerate(anchorMap):
        ax.scatter(anchorMap[anchor]["x"],anchorMap[anchor]["y"],anchorMap[anchor]["z"], c='blue')
        ax.text(anchorMap[anchor]["x"],anchorMap[anchor]["y"],anchorMap[anchor]["z"], anchor)

    ax.plot(coord[0],coord[1],coord[2],'.', c='green')
    fig.canvas.draw()

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(variance[0],label="var x")
    ax1.plot(variance[1],label="var y")
    ax1.plot(variance[2],label="var z")
    ax1.legend()

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(pHigh,label="highest probability")
    ax2.legend()
    #fig1.show()

if __name__ == "__main__":
    main()