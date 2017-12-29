import operator
import os

from SolarSystem import SolarSystem
from Playfield import *
from planet import SectorPlanet

sectorFolders = []
playfieldFolders = []
planets = {}
folder = 'C:\\games\\Steam\\steamapps\\common\\Empyrion - Galactic Survival\\Content'

basePlanets = ['Sun', 'Aestus Orbit', 'Akua Orbit', 'Skillon Orbit', 'Alien Outpost', 'Trading Outpost',
               'Omicron Orbit', 'Aitis Orbit', 'Masperon Orbit', 'Tallodar Orbit',
               'Ningues Orbit', 'Asteroid Field', 'Zeyhines Orbit', 'Oscutune Orbit', 'Instance Orbit',
               'Elemental Space Race Mission', 'Top Gun Mission']
starterPlanets =['Omicron Orbit','Akua Orbit']


def parsePlanet(path):
    playName = path.split('\\')[-2]
    obj = Playfield(playName)
    obj.parse(path)
    planets[obj.playfieldName] = obj
    if (obj.get('PlayfieldType') == 'Planet'):
        obj.report()


def getFromRing(ring, idx) :
    if idx < len(ring) and idx > 0 :
        return ring[idx]
    if idx < 0 :
        return ring[idx]
    return ring[idx - len(ring)]

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.lower() == 'sectors.yaml':
            sectorFolders.append(root + '\\' + file)

        if file.lower() == 'playfield.yaml':
            playfieldFolders.append(root + '\\' + file)

for item in playfieldFolders:
    parsePlanet(item)

for item in sectorFolders:
    sector = SolarSystem.parseSector(item, planets)
    print(len(sector.sectors), 'planets')

    # move the planets around based on their difficulity
    # make several rings with 1-2 transitions between each ring
    rings = 3
    minDiff = 999
    maxDiff = -999
    newPlanets = sector.getNewPlanets()
    existingPlanets = sector.getExistingPlanets()
    for i in  newPlanets:
        diff = i.getDiff()
        if diff < minDiff:
            minDiff = diff
        if diff > maxDiff:
            maxDiff = diff
    #print("min", minDiff, "max", maxDiff)
    ranges = (maxDiff - minDiff) / rings

    planetRings = []
    ringSize = math.floor(len(newPlanets) / rings)
    sector.sectors.sort(key=operator.methodcaller('getDiff'))

    offset=0
    batch = []
    for i in range(len(newPlanets)) :
        batch.append(newPlanets[i])
        if len(batch) >= ringSize :
           planetRings.append(batch)
           batch=[]
    if len(batch) > 0 :
       planetRings[-1].extend(batch)

    rad = 200
    pi2 = 3.14159265358 * 2
    for ring in planetRings :
        k = 0
        for pl in ring :
            pl.deny = []
            pl.deny.extend(starterPlanets)
            if len(ring) > 5 :
                pl.deny.append(getFromRing(ring,k-2).name)
                pl.deny.append(getFromRing(ring,k-3).name)
                pl.deny.append(getFromRing(ring,k+2).name)
                pl.deny.append(getFromRing(ring,k+3).name)

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
                dist = e.distanceTo(pl)
                #if pl.name == 'GX Feng Pho-Pho Orbit' :
                #    print('break')
                if dist < 250 :
                    e.deny.append(pl.name)
                    pl.deny.append(e.name)

        rad += 200

    worldName = item.split('\\')[-3]
    sector.write(worldName+'-Sectors.yaml')
