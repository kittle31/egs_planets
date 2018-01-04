import operator
import os

from SolarSystem import SolarSystem
from Playfield import *

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
    sector.makeRings(3)

    #remove connections between rings
    if len(sector.planetRings) > 0 :
        ringTo = sector.planetRings[0]
        for ringFrom in sector.planetRings :
            if ringFrom == ringTo:
                continue
            for plFrom in ringFrom :
                for plTo in ringTo :
                    dist = plFrom.distanceTo(plTo)
                    if dist < 250 :
                        plFrom.addDeny(plTo.name)
                        plTo.addDeny(plFrom.name)

            ringTo = ringFrom

    worldName = item.split('\\')[-3]
    sector.write(worldName+'-Sectors.yaml')
