import math
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
from random import uniform
import numpy as np
import time


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
        self.w = 0

        # Coordinates of the anchors in the system (all of them)
        self.map = map

        # Dictionary with all ddist for the particle
        # key = anchor id, val = ddist
        self.ddistDict = {}

        # The id of the master anchor
        self.refAnchor = reafAnchor

        # Calculates the ddist for the particle
        self.calculateDdist()

    def calculateDdist(self):
        # Distance to the ref_anchor (ref_ancor is in 0,0,0 by deffenition)
        refAnchorDist = math.sqrt(self.x**2 + self.y**2 + self.z**2)

        # Calculate the ddist to all other anchors. ddist is the difference in lenght from the ref_anchor to another anchor.
        for landmark in self.map:
            # Coordinate for that anchor (landmark)
            pos = landmark['pos']
            #print(pos['x'])
            #landmark = Ddist(self.x,self.y,self.z,landmark)
            #self.landmarks.append[landmark]

            # Euclidean distance differnece from with regards to the ref_anchor
            ddist = math.sqrt((pos['x']-self.x)**2 + (pos['y']-self.y)**2 + (pos['z']-self.z)**2)
            ddist = ddist - refAnchorDist
            self.ddistDict[landmark['addr']] = ddist


''' Move particles 
Move particle according to the integral of acceleration
time between latest measurment and the one before that.
Dist to move = acceleration * time
'''
def moveParticles(particles,measurment):

    # Time difference between this and last measurment
    timestep = measurment.ts - lastts

    # Acceleration in for this measurment
    ax = measurment['acc'][0]
    ay = measurment['acc'][1]
    az = measurment['acc'][2]

    # Distance to move all particles
    dx = ax*timestep
    dy = ay*timestep
    dz = az*timestep

    # Variance of the accelerometers measurement
    varAcc = 0.1

    return 0

''' Update map in particles'''
def updateMap(particles)
    return 0

''' Calculate ddist '''
def updateDdist(particles):

    return particles

''' Normalize weight 
Calculates the sum of all weights and normalize the weight for all particles'''
def normalizeWeight(particles):

    weightSum = 0
    # Sumation of all weights
    for particle in particles:
        weightSum = particle.w + weightSum

    # Normalization of the weights
    for particle in particles:
        particle.w = particle.w/ weightSum

    return 0



''' Assign Weight '''
def assignWeight(particles,measurment):
    
    # The meausurment
    mean = 0

    # Needs to be calculated before (or updated during)
    # !!!!!!!! NEEDS TO BE CHANGED !!!!!!!!
    cov = [[0.02,0,0],[0,0.2,0],[0,0,0.2]]
    # !!!!!!!! NEEDS TO BE CHANGED !!!!!!!!

    #Calculates the probability of that particle
    p = multivariate_normal.pdf(ddist, mean, cov)
    return particles

''' Init
m - number of particles
'''
def init(numParticles,map,minmax):
    particles = []
    
    # Search for the refernace anchor
    for j in range(0,len(map)):
        if map[j]["ref_anchor"] == 1:
            refAnchor = map[j]["addr"] 
            

    # Init uniform random position for all particles
    for i in range(0,numParticles):
        x = uniform(minmax['maxx'], minmax['minx'])
        y = uniform(minmax['maxy'], minmax['miny'])
        z = uniform(minmax['maxz'], minmax['minz'])

        # Create a particle
        particle = Particle(x,y,z,map,refAnchor)

        # Add particle
        particles.append(particle)

    return particles


''' Low variance sampling '''
def lowVarianceSampling(particles):

    return particles

''' Calculate histogram'''
def calculateHistogram(particles)

    return histogram

''' Most likely position
The most likely position of the tag given all the particles'''
def bestPos(particles)

    histogram = calculateHistogram(particles)

    return mu

''' Particle filter '''
def particleFilter(particles):

    # Calculate weight
    assignWeight(particles,measurment)

    # Normalize weight
    normalizeWeight(particles)

    # Resample
    lowVarianceSampling(particles)

    # Move particles
    moveParticles(particles,measurment)    

    mu = bestPos(particles)

    return (particles, mu)


''' Main
map - coordinates for landmarks
'''
def main():

    # Dummy map
    mapfile = open("map.json","r")
    mapstr = mapfile.read()
    map = json.loads(mapstr)

    # Number of particles 
    numParticles = 100

    # Between what coordinates the particles should be initialized 
    minmax = {
    "maxx":10,
    "minx":0,
    "maxy":10,
    "miny":0,
    "maxz":10,
    "minz":0,
    }

    # Init particles
    particles = init(numParticles, map, minmax)

    ###### For debugg 
    print(particles[0].ddistDict)
    #####
    
    # Visualisation
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for landmark in map:
        ax.scatter(landmark["pos"]['x'],landmark["pos"]['y'],landmark["pos"]['z'],c='blue')
    #plt.show()


    while (1):
        # Call the particle filter
        (particles,mu) = particleFilter(particles)
        
        # Display the particles and anchors 
        for particle in particles:
            ax.scatter(particle.x,particle.y,particle.z, c='red')
        ax.scatter(mu.x,mu.y,mu.z, c='black')
        fig.canvas.draw()
        fig.canvas.flush_events()
        

    
main()