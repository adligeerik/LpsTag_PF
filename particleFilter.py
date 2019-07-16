import math
from random import uniform


''' ddist class '''
class Ddist:
    __init__(self, id, pos):
        self.id = id
        self.x = pos.x
        self.y = pos.y
        self.z = pos.z

''' Particle Class
x,y,z - coordinates
map - positions of all landmarks (acnchors)
'''
class Particle:
    __init__(self,x,y,z,map):

        self.x = x
        self.y = y
        self.z = z

        self.map = map

        # key = anchor id, val = ddist
        self.ddistDict = {}
        self.refAnchor = reafAnchor

    def calculateDdist(self):
        refAnchorDist = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        for landmark in map:
            #landmark = Ddist(self.x,self.y,self.z,landmark)
            #self.landmarks.append[landmark]
            ddist = math.sqrt((landmark.x-self.x)**2 + (landmark.y-self.y)**2 + (landmark.z-self.z)**2)
            ddist = dist - refAnchorDist
            ddistDict[landmarj.id] = [dist]


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
    for i in range(0,numParticles):

        x = uniform(minmax{maxx}, minmax{minx})
        y = uniform(minmax{maxy}, minmax{miny})
        z = uniform(minmax{maxz}, minmax{minz})

        particles.append(Particle())
    return particles


''' Low variance sampling '''
def lowVarianceSampling(particles):

    return particles


''' Particle filter '''
def particleFilter(particles):

    return particles, mu


''' Main
map - coordinates for landmarks
'''
def main():


    numParticles = 100

    minmax = {
    "maxx":10,
    "minx":10,
    "maxy":10,
    "miny":10,
    "maxz":10,
    "minz":10,
    }

    init(numParticles, map, minmax)
    while (data):
