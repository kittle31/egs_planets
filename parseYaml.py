import operator
import os
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

def writeSector(path, sector):
    file = open(path, 'w')
    for item in sector:
        item.write(file)
    file.close()


def parseSector(path):
    # print(root, file)
    with open(path, 'rb')  as fileHandle:
        string = fileHandle.read()
    string = string.replace(b"\t", b"")
    obj = yaml.load(string)
    if type(obj).__name__ == 'list':
        planetList = obj
    else:
        planetList = obj['Sectors']
    print(path)
    planetSectors = []
    for item in planetList:
        planetSectors.append(SectorPlanet.loadFrom(item, planets))

    return planetSectors


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
    sector = parseSector(item)
    print(len(sector), 'planets')

    # move the planets around based on their difficulity
    # make several rings with 1-2 transitions between each ring
    rings = 3
    minDiff = 999
    maxDiff = -999
    newPlanets = [x for x in sector if x.name not in basePlanets]
    existingPlanets = [x for x in sector if x.name in basePlanets]
    for i in  newPlanets:
        diff = i.getDiff()
        if diff < minDiff:
            minDiff = diff
        if diff > maxDiff:
            maxDiff = diff
    print("min", minDiff, "max", maxDiff)
    ranges = (maxDiff - minDiff) / rings

    planetRings = []
    ringSize = math.floor(len(newPlanets) / rings)
    sector.sort(key=operator.methodcaller('getDiff'))

    offset=0
    for i in range(rings) :
        planetRings.append( newPlanets[offset:offset+ringSize])
        offset+=ringSize
    print(planetRings)

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
            print(pl.name, math.floor(newX), 30, math.floor(newZ))
            pl.location[0] = math.floor(newX)
            pl.location[1] = 0
            pl.location[2] = math.floor(newZ)
            k+=1
        rad += 200
    worldName = item.split('\\')[-3]
    writeSector(worldName+'-Sectors.yaml', sector)
