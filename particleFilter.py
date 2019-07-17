import math
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import uniform
import numpy as np
import time

''' Particle Class
x,y,z - coordinates
map - positions of all landmarks (acnchors)
'''
class Particle:
    def __init__(self,x,y,z,map,reafAnchor):

        self.x = x
        self.y = y
        self.z = z
        self.w = 0

        self.map = map

        # key = anchor id, val = ddist
        self.ddistDict = {}
        self.refAnchor = reafAnchor

        self.calculateDdist()

    def calculateDdist(self):
        refAnchorDist = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        for landmark in self.map:
            pos = landmark['pos']
            #print(pos['x'])
            #landmark = Ddist(self.x,self.y,self.z,landmark)
            #self.landmarks.append[landmark]
            ddist = math.sqrt((pos['x']-self.x)**2 + (pos['y']-self.y)**2 + (pos['z']-self.z)**2)
            ddist = ddist - refAnchorDist
            self.ddistDict[landmark['addr']] = ddist


''' Move particles '''
def moveParticles(particles):

    return particles

''' Calculate ddist '''
def updateDdist(particles):

    return particles

''' Normalize weight '''
def normalizeWeight(particles):

    return particles


''' Assign Weight '''
def assignWeight(particles):

    return particles

''' Init
m - number of particles
'''
def init(numParticles,map,minmax):
    particles = []
    
    for j in range(0,len(map)):
        #print(map[j])
        if map[j]["ref_anchor"] == 1:
            refAnchor = map[j]["addr"] 
            #print(refAnchor)

    for i in range(0,numParticles):
        #print(i)
        x = uniform(minmax['maxx'], minmax['minx'])
        y = uniform(minmax['maxy'], minmax['miny'])
        z = uniform(minmax['maxz'], minmax['minz'])


        particles.append(Particle(x,y,z,map,refAnchor))
    return particles


''' Low variance sampling '''
def lowVarianceSampling(particles):

    return particles


''' Particle filter '''
def particleFilter(particles):

    return (particles, mu)


''' Main
map - coordinates for landmarks
'''
def main():

    #Dummy map
    mapfile = open("map.json","r")
    mapstr = mapfile.read()
    map = json.loads(mapstr)

    #Number of particles 
    numParticles = 100

    #Between what coordinates the particles should be initialized 
    minmax = {
    "maxx":10,
    "minx":0,
    "maxy":10,
    "miny":0,
    "maxz":10,
    "minz":0,
    }

    #Init particles
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
        (particles,mu) = particleFilter(particles)
        
        for particle in particles:
            ax.scatter(particle.x,particle.y,particle.z, c='red')

        ax.scatter(mu.x,mu.y,mu.z, c='black')

        fig.canvas.draw()
        fig.canvas.flush_events()
        

    
main()