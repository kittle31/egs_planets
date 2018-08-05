import math
import random
import operator
from ruamel.yaml import YAML
yaml = YAML()

from planet import SectorPlanet

basePlanets = ['Sun', 'Aestus Orbit', 'Akua Orbit', 'Skillon Orbit', 'Alien Outpost', 'Trading Outpost',
               'Omicron Orbit', 'Aitis Orbit', 'Masperon Orbit', 'Tallodar Orbit',
               'Ningues Orbit', 'Asteroid Field', 'Zeyhines Orbit', 'Oscutune Orbit', 'Instance Orbit',
               'Sienna Orbit', 'Roggery Orbit',
               'Elemental Space Race Mission', 'Top Gun Mission']
starterPlanets = ['Omicron Orbit', 'Akua Orbit']


def getFromRing(ring, idx):
    if idx < len(ring) and idx > 0:
        return ring[idx]
    if idx < 0:
        return ring[idx]
    return ring[idx - len(ring)]


class SolarSystem:
    def __init__(self):
        self.path = ''
        self.sectors = []
        self.minDiff = None
        self.maxDiff = None
        self.planetRings = []

    @staticmethod
    def loadFrom(yml, planetDb):
        if type(yml).__name__ == 'CommentedSeq':
            planetList = yml
        else:
            planetList = yml['Sectors']
        solar = SolarSystem()
        for item in planetList:
            pl = SectorPlanet.loadFrom(item, planetDb)
            if len(pl.playfields) > 0:
                solar.sectors.append(pl)
        return solar

    @staticmethod
    def parseSector(path, planetDb):
        # print(root, file)
        with open(path, 'rb')  as fileHandle:
            string = fileHandle.read()
        string = string.replace(b"\t", b"")
        obj = yaml.load(string)

        solar = SolarSystem.loadFrom(obj, planetDb)
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
        print('wrote', path)

    def sortDifficulty(self):
        # sort the planets by difficulty

        self.minDiff = 999
        self.maxDiff = -999
        newPlanets = self.getNewPlanets()

        for i in newPlanets:
            diff = i.getDiff()
            if diff < self.minDiff:
                self.minDiff = diff
            if diff > self.maxDiff:
                self.maxDiff = diff
        self.sectors.sort(key=operator.methodcaller('getDiff'))

    def makeRings(self, rings):
        # move the planets around based on their difficulity
        # make several rings with 1-2 transitions between each ring
        self.sortDifficulty()
        existingPlanets = self.getExistingPlanets()
        newPlanets = self.getNewPlanets()

        initialRadius = 350
        radInc = 260
        pi = 3.14159265358
        planetDist = 150

        self.planetRings = []
        batch = []
        rad = initialRadius
        angle = planetDist / rad

        if len(newPlanets) == 0 :
            return
        radians = -pi
        dist = 0
        for planet in newPlanets:
            x = rad * math.cos(radians)
            y = rad * math.sin(radians)
            planet.location[0] = math.floor(x)
            planet.location[1] = 0
            planet.location[2] = math.floor(y)
            batch.append(planet)

            dist += planetDist
            radians += angle

            if radians > pi :
                self.planetRings.append(batch)
                batch = []
                rad += radInc
                planetDist += 30
                if planetDist > 200 :
                    planetDist = 200
                angle = planetDist / rad
                radians = -pi

        if len(batch) > 0:
            self.planetRings.append(batch)

        for ring in self.planetRings:
            k = 0
            for pl in ring:
                pl.allow = []
                pl.deny = []
                pl.deny.extend(starterPlanets)

                if len(ring) > 5:
                    pl.disconnectFrom(getFromRing(ring, k - 2))
                    pl.disconnectFrom(getFromRing(ring, k - 3))
                    pl.disconnectFrom(getFromRing(ring, k + 2))
                    pl.disconnectFrom(getFromRing(ring, k + 3))
                k += 1

                for e in existingPlanets:
                    if e.name != 'Sun':
                        dist = e.distanceTo(pl)
                        if dist < 251:
                            e.disconnectFrom(pl)
            rad += radInc
        self.removeExtraConnections()
        self.connectRingsToDefault()

    def removeExtraConnections(self):
        # remove connections between rings
        if len(self.planetRings) > 0:
            ringTo = self.planetRings[0]
            for ringFrom in self.planetRings:
                if ringFrom == ringTo:
                    continue
                for plFrom in ringFrom:
                    for plTo in ringTo:
                        dist = plFrom.distanceTo(plTo)
                        if dist < 250 :
                            plFrom.disconnectFrom(plTo)

                ringTo = ringFrom

    def connectRingsToDefault(self):
        # connect the rings to each other and to the starting planets

        connections = 3

        for idx in range(len(self.planetRings)):
            fromRing = self.planetRings[idx]
            if idx + 1 >= len(self.planetRings):
                continue
            toRing = self.planetRings[idx + 1]

            pickedSystems = []
            for i in range(connections):
                fromSystem = random.choice(toRing)
                while fromSystem in pickedSystems :
                    fromSystem = random.choice(fromRing)
                # find system in next ring closest to this system
                closest = fromRing[0]
                for planet in fromRing:
                    distFrom = fromSystem.distanceTo(planet)
                    distClose = fromSystem.distanceTo(closest)
                    if distFrom < distClose:
                        closest = planet

                distFrom = fromSystem.distanceTo(closest)
                print("ring",idx,"to",idx+1,"connect from", fromSystem.name, "to", closest.name, "dist",distFrom)
                closest.connectTo(fromSystem)
                pickedSystems.append(fromSystem)

        if len(self.planetRings) == 0:
            return
        # connect inner ring to starter planets
        for pName in starterPlanets:
            starterPlanet = [x for x in self.sectors if x.name == pName]
            if len(starterPlanet) == 0:
                continue
            starterPlanet = starterPlanet[0]
            closest = self.planetRings[0][0]
            for planet in self.planetRings[0]:
                dist = planet.distanceTo(starterPlanet)
                distClose = closest.distanceTo(starterPlanet)
                if dist < distClose:
                    closest = planet

            print("connect from", starterPlanet.name, "to", closest.name)
            starterPlanet.connectTo(closest)

        # connect any base planets that are < 15 AU
        for pName in basePlanets :
            basePlanet = [x for x in self.sectors if x.name == pName]
            if len(basePlanet) == 0:
                continue
            basePlanet = basePlanet[0]
            for planet in self.planetRings[0] :
                dist = planet.distanceTo(basePlanet)
                if dist < 150 :
                   planet.connectTo(basePlanet)

    def makeWeb(self):
        #reconnect the planets into a nice web
        if len(self.sectors) < 4 :
            return

        connections = 4
        for planet in self.sectors :
            if planet.isSun():
                continue

            planet.clearDeny()
            planet.clearAllow()

        for item in self.sectors:
            if item.isSun():
                continue
            distances = []
            for item1 in self.sectors :
                if item1==item or item1.isSun() :
                    continue
                dist = item.distanceTo(item1)
                distances.append((dist, item1))
            distances.sort(key=operator.itemgetter(0))

            conn = 0
            for distPlanet in distances :
                if conn < connections and len(item.allow) < connections :
                    item.connectTo( distPlanet[1])
                    conn +=1
                else :
                    if item.isConnectedTo(distPlanet[1]):
                        continue
                    if distPlanet[0] < 250 :
                        item.disconnectFrom( distPlanet[1])
