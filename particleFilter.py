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


''' Particle Class
x,y,z - coordinates
map - positions of all landmarks (acnchors)
'''
class Particle:
    def __init__(self,x,y,z,map,reafAnchor):

        # Coordinates of particle
        self.x = x
        self.y = y
        self.z = z

        # Weight of particle (init 0)
        self.weight = 0

        # Coordinates of the anchors in the system (all of them)
        self.map = map

        # Dictionary with all ddist for the particle
        # key = anchor id, val = ddist
        self.ddistDict = OrderedDict() 

        # The id of the master anchor
        self.refAnchor = reafAnchor

        # Calculates the ddist for the particle
        self.calculateDdist()

    def calculateDdist(self):
        # Distance to the ref_anchor (ref_ancor is in 0,0,0 by deffenition)
        refAnchorDist = math.sqrt(self.x**2 + self.y**2 + self.z**2)

        # Calculate the ddist to all other anchors. ddist is the difference in lenght from the ref_anchor to another anchor.
        for anchor in self.map:
            # Coordinate for that anchor (landmark)
            pos = self.map[anchor]

            # Euclidean distance differnece from with regards to the ref_anchor
            ddist = math.sqrt((pos['x']-self.x)**2 + (pos['y']-self.y)**2 + (pos['z']-self.z)**2)
            ddist = ddist - refAnchorDist
            self.ddistDict[anchor] = ddist


''' Move particles 
Move particle according to the integral of acceleration
time between latest measurment and the one before that.
Dist to move = acceleration * time
'''
def moveParticles(particles,acceleration,timestamp):

    # Time difference between this and last measurment
    timestep = 0.001 # timestamp - lastts

    # Acceleration in for this measurment
    #ax = acceleration[0]
    #ay = acceleration[1]
    #az = acceleration[2]

    ax = gauss(0,0.01)/14
    ay = gauss(0,0.01)/14
    az = gauss(0,0.01)/14

    # Distance to move all particles
    dx = ax*timestep
    dy = ay*timestep
    dz = az*timestep

    # Variance of the accelerometers measurement
    varAcc = 1

    for particle in particles:
        particle.x = particle.x + dx + gauss(0,varAcc)/10
        particle.y = particle.y + dy + gauss(0,varAcc)/10
        particle.z = particle.z + dz + gauss(0,varAcc)/10

    return 0

''' Update map in particles'''
def updateMap(particles):
    return 0

''' Calculate ddist '''
def updateDdist(particles):
    for particle in particles:
        particle.calculateDdist()
    

''' Normalize weight 
Calculates the sum of all weights and normalize the weight for all particles'''
def normalizeWeight(particles):

    weightSum = 0
    # Sumation of all weights
    for particle in particles:
        weightSum = particle.weight + weightSum

    # Normalization of the weights
    for particle in particles:
        particle.weight = particle.weight / weightSum

    weightSum = 0
    for particle in particles:
        weightSum = particle.weight + weightSum



''' Assign Weight '''
def assignWeight(particles,measurement):
    
    anchorOrder = []
    mean = []
    for anchor in measurement:
        anchorOrder.append(anchor["addr"])
        mean.append(anchor["ddist"])

    # Needs to be calculated before (or updated during)
    # !!!!!!!! NEEDS TO BE CHANGED !!!!!!!!
    variance = 0.002
    n = len(anchorOrder)
    cov = [] 

    for i in range(len(anchorOrder)):
        var = [0]*n
        var[i]= variance
        cov.append(var)
    # !!!!!!!! NEEDS TO BE CHANGED !!!!!!!!

    for particle in particles:
        ddist = []
        for anchor in anchorOrder:
            ddist.append(particle.ddistDict[anchor])
        
        
        mean = map(float,mean)

        #Calculates the probability of that particle
        p = multivariate_normal.pdf(ddist, mean, cov)
        particle.weight = p

    return particles

''' Init
m - number of particles
'''
def init(numParticles,map,minmax):
    particles = []
    
    # Search for the refernace anchor
    for i, anchor in enumerate(map):
        if map[anchor]["ref_anchor"] == 1:
            refAnchor = anchor 
            

    # Init uniform random position for all particles
    for i in range(0,numParticles):
        x = uniform(minmax['maxx'], minmax['minx'])
        y = uniform(minmax['maxy'], minmax['miny'])
        z = uniform(minmax['maxz'], minmax['minz'])

        # Create a particle
        try:
            particle = Particle(x,y,z,map,refAnchor)
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
    c = particles[0].weight
    i = 0
    for m in range(M):
        U = r + m*inM
        while( U > c ):
            i = i + 1
            c = c + particles[i].weight
        newParticles.append(copy.deepcopy(particles[i]))

    return(newParticles)



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

''' Most likely position
The most likely position of the tag given all the particles'''
def bestPos(particles):

    #histogram = calculateHistogram(particles)
    mu = highestWeight(particles)
    return mu

''' Particle filter '''
def particleFilter(particles,dataPackage):

    measurement = dataPackage["meas"]
    acceleration = dataPackage["acc"]
    acceleration = acceleration.replace('"','')
    acceleration = acceleration.replace('[','')
    acceleration = acceleration.replace(']','')
    acceleration = acceleration.split(',')
    acceleration = map(float, acceleration)
    timestep = dataPackage["ts"]

    # Calculate weight
    assignWeight(particles,measurement)

    # Normalize weight
    normalizeWeight(particles)

    # Resample
    particles = lowVarianceSampling(particles)
    
    # Move particles
    moveParticles(particles,acceleration,timestep)    

    updateDdist(particles)

    mu = bestPos(particles)

    return (particles, mu)


''' Main
map - coordinates for landmarks
'''
def main():

    # Read map
    mapfile = open("extra/coordinates.json","r")
    mapstr = mapfile.read()
    anchorMap = json.loads(mapstr)


    # Number of particles 
    numParticles = 1000

    # Between what coordinates the particles should be initialized 
    xAnchor = []
    yAnchor = []
    zAnchor = []
    for i, anchor in enumerate(anchorMap):
        xAnchor.append(anchorMap[anchor]["x"])
        yAnchor.append(anchorMap[anchor]["y"])
        zAnchor.append(anchorMap[anchor]["z"])

    # 1.2 is arbitrary choosen to have some particles outside of the anchors
    minmax = {
    "maxx":max(xAnchor)*1.2,
    "minx":min(xAnchor)*1.2,
    "maxy":max(yAnchor)*1.2,
    "miny":min(yAnchor)*1.2,
    "maxz":max(zAnchor)*1.2,
    "minz":min(zAnchor)*1.2,
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

    ax.set_xlim3d(xmean-span,xmean+span)
    ax.set_ylim3d(ymean-span,ymean+span)
    ax.set_zlim3d(zmean-span,zmean+span)

    # Read file with tag data for simulation
    tagdata = open("tagdata/tagdata.json","r")

    for line in tagdata:
        ax.clear()
        ax.set_xlim3d(xmean-span,xmean+span)
        ax.set_ylim3d(ymean-span,ymean+span)
        ax.set_zlim3d(zmean-span,zmean+span)

        dataPackage = json.loads(line)

        # Draw anchors
        for i, anchor in enumerate(anchorMap):
            ax.scatter(anchorMap[anchor]["x"],anchorMap[anchor]["y"],anchorMap[anchor]["z"], c='blue')
            ax.text(anchorMap[anchor]["x"],anchorMap[anchor]["y"],anchorMap[anchor]["z"], anchor)
        
        # Call the particle filter
        (particles,mu) = particleFilter(particles,dataPackage)
        
        # Display the particles
        #for particle in particles:
        #    ax.scatter(particle.x,particle.y,particle.z, c='red')

        ax.scatter(mu["x"],mu["y"],mu["z"], c='green')

        fig.canvas.draw()
        fig.canvas.flush_events()
        #raw_input("Press Enter to continue...")



main()