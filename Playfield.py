import math
import  yaml

class Playfield:
    #playfield.yaml
    def __init__(self, playfieldName=None):
        self.path = ''
        self.obj = {}
        self.playfieldName = playfieldName
        self.TemperatureDay = None
        self.TemperatureNight = None
        self.playType = None
        self.terrainType = None

    def parse(self, path):
        self.path = path
        with open(self.path, 'rb')  as fileHandle:
            string = fileHandle.read()
            string = string.replace(b"\t", b"")
            self.obj = yaml.load(string)

        self.TemperatureDay = self.obj.get('TemperatureDay', None)
        self.TemperatureNight = self.obj.get('TemperatureNight', None)
        self.playType = self.obj.get('PlayfieldType')
        if self.playType == 'Planet' :
           obj = self.get('Terrain')
           if obj is None :
              print('no terrain name', path)
           else:
              self.terrainType = obj.get('Name', None)

    def get(self, key):
        return self.obj.get(key, None)

    def report(self):
        print(self.terrainType, ',',self.playfieldName, ',' ,self.playType, ',', self.get('Difficulty'), ',',  self.TemperatureDay, self.TemperatureNight)

    def getDiff(self):
        # diff for this planet
        tempScale = 0.15
        droneScale = 0.5
        radScale = 0.75

        diff = self.get('Difficulty')
        atmo = self.get('AtmosphereBreathable')
        if atmo is not None :
            if atmo :
                diff -=1
            else:
                diff +=1
        rad = self.get('Radiation')
        if rad is not None :
            diff += math.floor(rad*radScale)

        pvp = self.get('PvP')
        if pvp is not None :
            if pvp :
                diff+=1
            else:
                diff-=1

        if self.get('PlayfieldType') == 'Planet' :
            temp = self.get('TemperatureDay')
            if temp is not None and temp > 40 :
                diff += math.floor((temp - 40) * tempScale)
            temp = self.get('TemperatureNight')
            if temp is not None and temp < 5 :
                diff += math.floor(abs(temp - 5) * tempScale)
        else :
            diff += 5

        drones = math.floor(self.getDroneCount() * droneScale)
        diff += drones
        if drones == 0 :
            diff -= 1

        poiCount = math.floor(self.getPOICount())
        diff += poiCount

        return diff

    def getDroneCount(self):
        #return average # of drones for this planet
        drones = 0
        sp = self.get('DroneSpawning')
        if sp is not None :
            random = sp.get('Random', [])
            for item in random :
                minmax = item.get('DronesMinMax', [])
                min = minmax[0]
                max = minmax[1]
                drones += ((max - min) / 2) + min

        poi = self.get('POIs')
        if poi is not None :
            for item in poi.get('Random', []) :
                if item.get('DroneBaseSetup', None) is not None :
                    minmax = item.get('DronesMinMax', [])
                    min = minmax[0]
                    max = minmax[1]
                    drones += ((max - min) / 2) + min

        return drones

    def getPOICount(self):
        #return the average number of generated POIs
        count = 0
        poi = self.get('POIs')
        if poi is not None :
            for item in poi.get('Random', []) :
                if item.get('GroupName', None) is not None :
                    minmax = item.get('CountMinMax', [])
                    min = minmax[0]
                    max = minmax[1]
                    count += ((max - min) / 2) + min

        return count