import math
import yaml
import operator


from planet import SectorPlanet

basePlanets = ['Sun', 'Aestus Orbit', 'Akua Orbit', 'Skillon Orbit', 'Alien Outpost', 'Trading Outpost',
               'Omicron Orbit', 'Aitis Orbit', 'Masperon Orbit', 'Tallodar Orbit',
               'Ningues Orbit', 'Asteroid Field', 'Zeyhines Orbit', 'Oscutune Orbit', 'Instance Orbit',
               'Elemental Space Race Mission', 'Top Gun Mission']
starterPlanets =['Omicron Orbit','Akua Orbit']

def getFromRing(ring, idx) :
    if idx < len(ring) and idx > 0 :
        return ring[idx]
    if idx < 0 :
        return ring[idx]
    return ring[idx - len(ring)]


class SolarSystem :
    def __init__(self):
        self.path=''
        self.sectors=[]
        self.minDiff = None
        self.maxDiff = None

    @staticmethod
    def loadFrom(yml, planetDb):
        if type(yml).__name__ == 'list':
            planetList = yml
        else:
            planetList = yml['Sectors']
        solar = SolarSystem()
        for item in planetList:
            pl = SectorPlanet.loadFrom(item, planetDb)
            if len(pl.playfields) > 0 :
                solar.sectors.append(pl)
        return solar

    @staticmethod
    def parseSector(path, planetDb):
        # print(root, file)
        with open(path, 'rb')  as fileHandle:
            string = fileHandle.read()
        string = string.replace(b"\t", b"")
        obj = yaml.load(string)

        solar =  SolarSystem.loadFrom(obj,planetDb)
        solar.path = path
        return solar

    def getNewPlanets(self):
        return [x for x in self.sectors if x.name not in basePlanets]

    def getExistingPlanets(self):
        return [x for x in self.sectors if x.name in basePlanets]

    def write(self, path):
        file = open(path, 'w')
        for item in self.sectors:
            item.write(file)
        file.close()

    def sortDifficulty(self):
        #sort the planets by difficulty

        self.minDiff = 999
        self.maxDiff = -999
        newPlanets = self.getNewPlanets()

        for i in newPlanets:
            diff = i.getDiff()
            if diff < self.minDiff:
                self.minDiff = diff
            if diff > self.maxDiff:
                self.maxDiff = diff
        # print("min", minDiff, "max", maxDiff)
        self.sectors.sort(key=operator.methodcaller('getDiff'))

    def makeRings(self, rings):
        # move the planets around based on their difficulity
        # make several rings with 1-2 transitions between each ring
        self.sortDifficulty()
        existingPlanets = self.getExistingPlanets()
        newPlanets = self.getNewPlanets()

        self.planetRings = []
        ringSize = math.floor(len(self.getNewPlanets()) / rings)
        batch = []
        for i in range(len(newPlanets)) :
            batch.append(newPlanets[i])
            if len(batch) >= ringSize :
               self.planetRings.append(batch)
               batch=[]
        if len(batch) > 0 :
           self.planetRings[-1].extend(batch)

        rad = 200
        pi2 = 3.14159265358 * 2
        for ring in self.planetRings :
            k = 0
            for pl in ring :
                pl.deny = []
                pl.deny.extend(starterPlanets)
                if pl.name == 'GX Baalat Orbit' :
                   print('break')

                if len(ring) > 5 :
                    pl.addDeny(getFromRing(ring,k-2).name)
                    pl.addDeny(getFromRing(ring,k-3).name)
                    pl.addDeny(getFromRing(ring,k+2).name)
                    pl.addDeny(getFromRing(ring,k+3).name)

                x=pl.location[0]
                z=pl.location[2]
                newX = rad * math.cos((k * pi2) / len(ring))
                newZ = rad * math.sin((k * pi2) / len(ring))
                #print(pl.name, math.floor(newX), 30, math.floor(newZ))
                pl.location[0] = math.floor(newX)
                pl.location[1] = 0
                pl.location[2] = math.floor(newZ)
                k+=1

                for e in existingPlanets:
                    if e.name != 'Sun' :
                        dist = e.distanceTo(pl)
                        if dist < 251 :
                            e.addDeny(pl.name)
                            pl.addDeny(e.name)
            rad += 200
