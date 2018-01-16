import math
import random

import yaml

from Resource import PlanetResource

keys = ['RealRadius',
        'ScaledRadius',
        'Gravity',
        'AtmosphereDensity',
        'AtmosphereO2',
        'AtmosphereBreathable',
        'TemperatureDay',
        'TemperatureNight',
        'Music',
        'Radiation',
        'DayLength',
        'PlanetType',
        'Moons',
        'Water',
        'SeaLevel',
        'PvP',
        'Seed',
        'UseFixed',
        'Difficulty',
        'PlayfieldType',
        'Description',
        'SunFlare',
        'AtmosphereEnabled',
        'AtmosphereColor',
        'SkyColor',
        'SkyHorizonColor',
        'DayLightIntensity',
        'NightLightIntensity',
        'DayShadowStrength',
        'NightLightColor',
        'AtmosphereFog',
        'FogCloudIntensity',
        'FogIntensity',
        'FogStartDistance',
        'GroundFogIntensity',
        'GroundFogHeight',
        'CloudsDensity',
        'CloudsSharpness',
        'CloudsBrightness',
        'CloudsOpacity',
        'CloudsZenithColor',
        'CloudsHorizonColor',
        'WindSpeed',
        'RandomResources',
        'AsteroidResources',
        'Terrain',
        'MainBiome'
        'SubBiomes'
        ]

terrainTypes = ['Temperate', 'Alien', 'Lava', 'Temperate2b', 'Barren', 'Desert', 'Desert2', 'DesertNew',
                'TemperateNew2', 'NewTemperate', 'NewAlien', 'NewSnow', 'NewDesert', 'NewDesert2', 'Lava2New',
                'NewTemperate500', 'NewAlien_V2', 'NewBarren', 'NewBarren_V2', 'NewDesert2_V2', 'NewDesert_V2',
                'NewLava', 'NewLava2', 'NewLava2_V2', 'NewLava_V2', 'NewOcean', 'NewOcean_V2', 'NewSnow_V2',
                'NewTemperate_V2', 'Snow', 'TemperateNew3', 'MountainAndValley', 'NewMoon2']

def randBool() :
    if random.randint(0,1) == 0 :
        return True
    else :
        return False

class Playfield:
    # playfield.yaml
    def __init__(self, playfieldName=None):
        self.path = ''
        self.obj = {}
        self.playfieldName = playfieldName
        self.TemperatureDay = random.randint(20,50)
        self.TemperatureNight = random.randint(-50,self.TemperatureDay)
        self.PlayfieldType = 'Planet'
        self.TerrainType = None
        self.Terrain = None

        self.extraProps = {}
        self.props = {}
        self.newTerrain()
        self.setDefaults()

    def setDefaults(self):
        #set default and static values
        self.props['RealRadius'] = 1303.797294
        self.props['ScaledRadius'] = 1300
        self.props['Gravity'] = random.uniform(-18,-4.5)
        self.props['AtmosphereDensity'] = random.uniform(0.25, 3)
        self.props['AtmosphereO2'] = random.uniform(0.01, 0.75)
        self.props['AtmosphereBreathable'] = randBool()

        self.props['Music'] = 'Hyperion'
        rad = random.uniform(-10, 10)
        if rad < 0 :
            rad = 0
        self.props['Radiation'] =rad
        self.props['DayLength'] = 24
        self.props['Moons'] = 1

        self.props['SeaLevel'] = random.randint(30, 70)
        self.props['PvP'] = randBool()

        self.props['AtmosphereEnabled'] = randBool()

        # Light
        self.props['DayLightIntensity'] = random.uniform(0.9, 1.2)
        self.props['NightLightIntensity'] = random.uniform(0.6, 1.0)

        # Fog
        self.props['AtmosphereFog'] = 0.15  # Distant fog, between 0 and 1: larger values = stronger
        self.props['FogCloudIntensity'] =  0.15  # Waft of mist in air, between 0 and 1: larger values = stronger
        self.props['FogIntensity']= 0.2  # Near Fog/Atmospheric Scattering Intensity, between 0 and 1: larger values = stronger
        self.props['FogStartDistance']= 200  # Near Fog/Atmospheric Scattering Start Distance, in m
        self.props['GroundFogIntensity']= .1  # Ground Layer Fog, between 0 and 1: larger values = stronger
        self.props['GroundFogHeight']= 35  # Ground Layer Fog Height

        # Clouds
        self.props['CloudsDensity']= 0.6  # Between 0 and 1: larger values = more clouds (coverage)
        self.props['CloudsSharpness']= 0.4  # Between 0 and 1: larger values = less dense clouds
        self.props['CloudsBrightness'] = 1  # Between 0 and 2: larger values = brighter clouds

        # Wind Speed
        self.props['WindSpeed'] = random.randint(0,10)

    def generateResources(self):
        resList = []
        resList.append(PlanetResource.random(1))
        resList.append(PlanetResource.random(1))
        resList.append(PlanetResource.random(1))
        self.props['RandomResources'] = resList


    def parse(self, path):
        self.path = path
        with open(self.path, 'rb')  as fileHandle:
            string = fileHandle.read()
            string = string.replace(b"\t", b"")
            obj = yaml.load(string)

        for key in obj:
            value = obj.get(key)
            if key in keys:
                self.props[key] = value
            else:
                self.extraProps[key] = value

        for key in self.__dict__:
            if key in self.props:
                setattr(self, key, self.props.get(key))

        if self.PlayfieldType == 'Planet':
            obj = self.get('Terrain')
            if obj is None:
                print('no terrain name', path)
            else:
                self.TerrainType = obj.get('Name', None)

    def write(self, path):
        with open(path, 'w') as file:
            for key in keys:
                if key in self.props:
                    value = self.props[key]
                    valueType = type(value).__name__
                    if valueType == 'dict' or valueType == 'list':
                        tmpDict = {key: self.props[key]}
                        yaml.dump(tmpDict, file)
                    else:
                        if valueType == 'str':
                            file.write(key + ": '" + str(value) + "'\n")
                        else:
                            file.write(key + ': ' + str(value) + '\n')

            yaml.dump(self.extraProps, file)

    def get(self, key):
        return self.props.get(key, None)

    def report(self):
        print(self.playfieldName, ',', self.TerrainType, ',',
              self.PlayfieldType, ',', self.get('Difficulty'), ',',
              self.TemperatureDay, ',',self.TemperatureNight,',',
              self.get('Terrain').get('PerlinCol', None),',',
              self.get('Terrain').get('NoiseStrength', None)
              )

    def removeGoldMeteor(self):
        toRemove = []
        meteors = self.obj.get('AsteroidResources', [])
        for item in meteors:
            if item.get('Name', '') == 'GoldResource':
                toRemove.append(item)
        for item in toRemove:
            meteors.remove(item)
            print('removed meteor', item, 'from', self.playfieldName)
        return len(toRemove) > 0

    def setPOIToRegen(self):
        # check each poi and make sure it has a regen attribute
        pois = self.get('POIs')
        if pois is None:
            return False
        changed = False
        for poi in pois.get('Random', []):
            if poi.get('GroupName', '') == 'Wreckage':
                continue
            if poi.get('Properties', None) is None:
                poi['Properties'] = []
            regenFound = False
            props = poi.get('Properties')
            for prop in props:
                if prop.get('Key', '') == 'RegenAfter':
                    regenFound = True
            if not regenFound:
                props.append({'Key': 'RegenAfter', 'Value': 720})
                print("add regen to", poi.get('GroupName', '<unnamed poi>'), 'in', self.playfieldName)
                changed = True

        return changed

    def fixDroneSetup(self):
        # ensure Dronebase setup has the right groupname
        drones = self.get('DroneBaseSetup')
        if drones is None:
            return False
        group = drones.get('GroupName', None)
        if group != 'DroneBaseSetup':
            drones['GroupName'] = 'DroneBaseSetup'
            print("fix dronebasesetup for", self.playfieldName)
            return True
        return False

    def getDiff(self):
        # diff for this planet
        tempScale = 0.15
        droneScale = 0.5
        radScale = 0.75

        diff = self.get('Difficulty')
        atmo = self.get('AtmosphereBreathable')
        if atmo is not None:
            if atmo:
                diff -= 1
            else:
                diff += 1
        rad = self.get('Radiation')
        if rad is not None:
            diff += math.floor(rad * radScale)

        pvp = self.get('PvP')
        if pvp is not None:
            if pvp:
                diff += 1
            else:
                diff -= 1

        if self.get('PlayfieldType') == 'Planet':
            temp = self.get('TemperatureDay')
            if temp is not None and temp > 40:
                diff += math.floor((temp - 40) * tempScale)
            temp = self.get('TemperatureNight')
            if temp is not None and temp < 5:
                diff += math.floor(abs(temp - 5) * tempScale)
        else:
            diff += 5

        drones = math.floor(self.getDroneCount() * droneScale)
        diff += drones
        if drones == 0:
            diff -= 1

        poiCount = math.floor(self.getPOICount())
        diff += poiCount

        return diff

    def getDroneCount(self):
        # return average # of drones for this planet
        drones = 0
        sp = self.get('DroneSpawning')
        if sp is not None:
            random = sp.get('Random', [])
            for item in random:
                minmax = item.get('DronesMinMax', [])
                min = minmax[0]
                max = minmax[1]
                drones += ((max - min) / 2) + min

        poi = self.get('POIs')
        if poi is not None:
            for item in poi.get('Random', []):
                if item.get('DroneBaseSetup', None) is not None:
                    minmax = item.get('DronesMinMax', [])
                    min = minmax[0]
                    max = minmax[1]
                    drones += ((max - min) / 2) + min

        return drones

    def getPOICount(self):
        # return the average number of generated POIs
        count = 0
        poi = self.get('POIs')
        if poi is not None:
            for item in poi.get('Random', []):
                if item.get('GroupName', None) is not None:
                    minmax = item.get('CountMinMax', [])
                    min = minmax[0]
                    max = minmax[1]
                    count += ((max - min) / 2) + min

        return count

    def newTerrain(self):
        # create a new terrain for the playfield
        self.Terrain = {
            'Name': random.choice(terrainTypes),
            'PoleLevel': 30,
            'NoiseStrength': random.uniform(0 , 1.5),
            'PerlinCol': random.uniform(0, 1.5),
            'ColorChange': {
                'YFadeCenter': 45,
                'YFadeRange': 20,
                'YFadeMin': -0.1,
                'YFadeMax': -0.15
            }
        }
        self.props['Terrain'] = self.Terrain
        self.TerrainType = self.Terrain['Name']

