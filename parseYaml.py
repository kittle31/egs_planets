import operator
import os

from SolarSystem import SolarSystem
from Playfield import *

sectorFolders = []
playfieldFolders = []
planets = {}
folder = 'E:\\games\\Steam\\steamapps\\common\\Empyrion - Galactic Survival\\Content'

basePlanets = ['Sun', 'Aestus Orbit', 'Akua Orbit', 'Skillon Orbit', 'Alien Outpost', 'Trading Outpost',
               'Omicron Orbit', 'Aitis Orbit', 'Masperon Orbit', 'Tallodar Orbit',
               'Ningues Orbit', 'Asteroid Field', 'Zeyhines Orbit', 'Oscutune Orbit', 'Instance Orbit',
               'Elemental Space Race Mission', 'Top Gun Mission']
starterPlanets =['Omicron Orbit','Akua Orbit']

def parsePlanet(path):
    global minNoise, maxNoise, minPerlin, maxPerlin

    parts = path.split('\\')
    playName = parts[-2]
    obj = Playfield(playName)
    print(path)
    obj.parse(path)
    planets[obj.playfieldName] = obj
    if (obj.get('PlayfieldType') == 'Planet'):
        obj.report()

    #obj.write(path + "1")
    if playName.startswith('GX ') :
        poi = obj.setPOIToRegen()
        met = obj.removeGoldMeteor()
        dron = obj.fixDroneSetup()
        if poi or met or dron :
            obj.write(path)

testP = Playfield()
testP.randomValues()
testP.write('E:\\games\\Steam\\steamapps\\common\\Empyrion - Galactic Survival\\Content\\Playfields\\testworld\\playfield.yaml')

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
    sector.removeExtraConnections()
    sector.connectRingsToDefault()

    worldName = item.split('\\')[-3]
    sector.write(worldName+'-Sectors.yaml')
