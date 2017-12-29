import yaml

from planet import SectorPlanet

basePlanets = ['Sun', 'Aestus Orbit', 'Akua Orbit', 'Skillon Orbit', 'Alien Outpost', 'Trading Outpost',
               'Omicron Orbit', 'Aitis Orbit', 'Masperon Orbit', 'Tallodar Orbit',
               'Ningues Orbit', 'Asteroid Field', 'Zeyhines Orbit', 'Oscutune Orbit', 'Instance Orbit',
               'Elemental Space Race Mission', 'Top Gun Mission']
starterPlanets =['Omicron Orbit','Akua Orbit']

class SolarSystem :
    def __init__(self):
        self.path=''
        self.sectors=[]

    @staticmethod
    def loadFrom(yml, planetDb):
        if type(yml).__name__ == 'list':
            planetList = yml
        else:
            planetList = yml['Sectors']
        solar = SolarSystem()
        for item in planetList:
            solar.sectors.append(SectorPlanet.loadFrom(item, planetDb))
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