import math
import random
from Resource import PlanetResource, MeteorResource

from ruamel.yaml import YAML
yaml = YAML(typ='unsafe')
yaml.boolean_representation = ['False', 'True']

keys = ['RealRadius',
        'ScaledRadius',
        'Gravity',
        'AtmosphereDensity',
        'AtmosphereO2',
        'AtmosphereBreathable',
        'Temperature',
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
        'Difficulty',
        'Seed',
        'UseFixed',
        'PlayfieldType',
        'Description',
        'SunFlare',
        'LocalEffect',
        'AtmosphereEnabled',
        'AtmosphereColor',
        'SkyColor',
        'SkyHorizonColor',
        'LightZenithColor',
        'LightHorizonColor',
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
        'MainBiome',
        'Biome',
        'SubBiomes',
        'POIs',
        'DroneSpawning',
        'DroneBaseSetup',
        'CreatureSpawning'
        ]

objectKeys = {'RandomResources' : PlanetResource, 'AsteroidResources' : MeteorResource}

terrainTypes = ['Temperate', 'Alien', 'Lava', 'Temperate2b', 'Barren', 'Desert', 'Desert2', 'DesertNew',
                'TemperateNew2', 'NewTemperate', 'NewAlien', 'NewSnow', 'NewDesert', 'NewDesert2', 'Lava2New',
                'NewTemperate500', 'NewBarren',
                'NewLava', 'NewLava2',  'NewOcean'
                #'NewTemperate_V2', 'Snow', 'TemperateNew3', 'NewMoon2',
                #'NewAlien_V2', 'NewLava2_V2', 'NewLava_V2', 'NewOcean_V2',
                #'NewSnow_V2', 'NewBarren_V2', 'NewDesert2_V2', 'NewDesert_V2',
                ]

waterTypes = ['WaterBlue', 'WaterGreen', 'WaterBrown', 'RockLava03']

sunFlareTypes = ['SunFlareBlue','SunFlareWhite', 'SunFlareWhite2',
                 'SunFlareWhite3', 'SunFlareYellow', 'SunFlarePurple']
biomeTextures = [
    'AlienBlack01',
'AlienGreen',
'AlienGreen06',
'AlienGreen07',
'Bedrock',
'BedrockLava',
'Clay',
'Cliff',
'CliffBrown',
'CliffDark',
'DirtCliff',
'Grass01BrownCliff',
'Grass02Cliff',
'Grass03Cliff',
'Grass05Cliff',
'GravelRockBrown03',
'RockBlack',
'RockBrown01',
'RockBrown03',
'RockGrassCliff',
'RockGrey08',
'RockGrey08Lava',
'RockGrey08Lava02',
'RockLava02',
'RockLava04',
'RockLava05',
'SandBeach',
'SandBeach01Cliff',
'SandYellow03Clay',
'SeaGround',
'SeaGround02',
'Snow08',
'Snow08Cliff',
'Snow08RockBrown03',
'SnowRock04',
'SnowyGrass',
'Stone',
'StoneBeach' ]

def randBool() :
    if random.randint(0,1) == 0 :
        return True
    else :
        return False

def uniformFloor(start, end, floor) :
    value = random.uniform(start, end)
    if value <= floor :
        value = floor
    return value

def intFloor(start, end, floor) :
    value = random.randint(start, end)
    if value <= floor :
        value = floor
    return value

def randomColor():
    r = uniformFloor(-0.1,1,0)
    g = uniformFloor(-0.1,1,0)
    b = uniformFloor(-0.1,1,0)
    return str(r)[0:4] + ', '+str(g)[0:4]+', '+str(b)[0:4]

class Playfield:
    # playfield.yaml
    def __init__(self, playfieldName=None):
        self.path = ''
        self.obj = {}
        self.playfieldName = playfieldName
        self.Temperature = None
        self.TemperatureDay = None
        self.TemperatureNight = None
        self.PlayfieldType = None
        self.TerrainType = None
        self.Terrain = None
        self.Water = None
        self.RandomResources = []

        self.extraProps = {}
        self.props = {}

    def randomValues(self):
        self.setDefaults()
        self.newTerrain()
        self.defaultBiome()
        self.generateResources()
        self.generatePOI()
        self.props['Description'] = self.props['Description'] + " "+self.props['Terrain']['Name']

    def setDefaults(self):
        #set default and static values
        self.TemperatureDay = random.randint(20,50)
        self.TemperatureNight = random.randint(-50,self.TemperatureDay)
        self.Temperature = int(( self.TemperatureDay + self.TemperatureNight) / 2)
        self.PlayfieldType = 'Planet'
        self.Water = random.choice(waterTypes)
        if self.Water == 'RockLava03' :
           self.props['Emissive'] = True

        self.props['RealRadius'] = 1303.797294
        self.props['ScaledRadius'] = 1300
        self.props['Gravity'] =           random.uniform(-18,-4.5)
        self.props['AtmosphereDensity'] = random.uniform(0.25, 3)
        self.props['AtmosphereO2'] =      random.uniform(0, 1)
        self.props['AtmosphereBreathable'] = randBool()

        self.props['Radiation']  = uniformFloor(-10, 10, 0)
        self.props['DayLength']  = 24
        self.props['Moons']      = 1

        self.props['SeaLevel']    = random.randint(20, 50)
        self.props['PvP']         = randBool()
        self.props['Difficulty']  = intFloor(0,5, 2)
        self.props['Description'] = 'Generated Planet'
        self.props['SunFlare']    = 'EnvironmentalEffects/' + random.choice(sunFlareTypes)
        self.props['LocalEffect'] = {'Name' : 'EnvironmentalEffects/Sparks', 'MaxHeight': 400}
        self.props['AtmosphereEnabled'] = randBool()
        self.props['AtmosphereColor']   = randomColor()
        self.props['SkyColor']          = randomColor()
        self.props['SkyHorizonColor']   = randomColor()

        # Light
        self.props['DayLightIntensity']   = random.uniform(0.5, 1.2)
        self.props['NightLightIntensity'] = random.uniform(0.4, 1.0)
        self.props['NightLightColor']     = randomColor()

        # Fog
        self.props['AtmosphereFog']      = uniformFloor(-0.5,1, 0)     # Distant fog, between 0 and 1: larger values = stronger
        self.props['FogCloudIntensity']  = uniformFloor(-0.1, 1, 0)    # Waft of mist in air, between 0 and 1: larger values = stronger
        self.props['FogIntensity']       = uniformFloor(-0.1, 1, 0.01) # Near Fog/Atmospheric Scattering Intensity, between 0 and 1: larger values = stronger
        self.props['FogStartDistance']   = 200    # Near Fog/Atmospheric Scattering Start Distance, in m
        self.props['GroundFogIntensity'] = uniformFloor(-0.5,1,0)    # Ground Layer Fog, between 0 and 1: larger values = stronger
        #set fog  height a little above sea level
        self.props['GroundFogHeight']    = self.props['SeaLevel'] + intFloor(-1,30,1)

        # Clouds
        self.props['CloudsDensity']      = uniformFloor(-0.1, 1, 0.1)  # Between 0 and 1: larger values = more clouds (coverage)
        self.props['CloudsSharpness']    = uniformFloor(-0.1, 1, 0)    # Between 0 and 1: larger values = less dense clouds
        self.props['CloudsBrightness']   = random.uniform(0,2)         # Between 0 and 2: larger values = brighter clouds
        self.props['CloudsZenithColor']  = randomColor()
        self.props['CloudsHorizonColor'] = randomColor()

        # Wind Speed
        self.props['WindSpeed'] = random.randint(0,30)

        #Drones
        self.props['DroneSpawning'] = {
        'Random' : [{
            'DronesMinMax': [5, 10],
            'CenterX': 2500,
            'Radius': 1500
            }]
        }

    def generateResources(self):
        self.RandomResources = PlanetResource.randomList()
        self.AsteroidResources = [x.makeMeteor() for x in self.RandomResources]
        self.AsteroidResources = [x for x in self.AsteroidResources if x is not None]

    def parse(self, path):
        self.path = path
        with open(self.path, 'rb')  as fileHandle:
            string = fileHandle.read()
            string = string.replace(b"\t", b"")
            string = string.replace(b"E-05", b".0E-05")
            string = string.replace(b"DayShadowStrength", b"DayShadowStrength1", 1)
            try :
                obj = yaml.load(string)
            except Exception as e:
                print(path)
                print(e)

        for key in obj:
            value = obj.get(key)
            if key in objectKeys :
                setattr(self, key, objectKeys[key].parse(value) )
                continue

            if key in keys:
                self.props[key] = value
                continue

            self.extraProps[key] = value

        for key in self.__dict__:
            if key in self.props:
                setattr(self, key, self.props.get(key))

        if self.PlayfieldType == 'Planet':
            obj = self.get('Terrain')
            if obj is not None:
                self.TerrainType = obj.get('Name', None)

    def write(self, path):
        self.preWrite()
        with open(path, 'w') as file:
            for key in keys:
                value = self.props.get(key, None)
                if value is None :
                    value = getattr(self, key,  None)
                if value is not None :
                    valueType = type(value).__name__
                    if valueType == 'dict' or valueType == 'list':
                        tmpDict = {key: value}
                        yaml.dump(tmpDict, file)
                    else:
                        if valueType == 'str':
                            file.write(key + ": '" + str(value) + "'\n")
                        else:
                            file.write(key + ': ' + str(value) + '\n')
            if len(self.extraProps) > 0 :
                yaml.dump(self.extraProps, file)

    def preWrite(self) :
        for key in objectKeys :
            value = getattr(self, key)
            result = [x.__dict__ for x in value]
            self.props[key] = result

    def get(self, key):
        v = self.props.get(key, None)
        if v is None :
            v = self.extraProps.get(key, None)
        return v

    @classmethod
    def reportHeader(cls):
        print('Name, TerrainType, PayfieldType, diff, TempDay, TempNite, PerlinCol, NoiseStrength, Tex1, Tex2, Tex3, Tex4')

    def report(self):
        b = self.get('MainBiome')
        t1=''
        t2=''
        t3=''
        t4=''
        pCol = ''
        noise = ''
        if self.get('Terrain') is not None :
            pCol = self.get('Terrain').get('PerlinCol', None)
            noise = self.get('Terrain').get('NoiseStrength', None)
        if b is not None:
            tex = b.get('Textures', None)
            t1 = tex[0]
            t2 = tex[1]
            t3 = tex[2]
            if len(tex) > 3 :
                t4 = tex[3]
            else :
                t4 = ''
        print(self.playfieldName, ',',
              self.TerrainType, ',',
              self.PlayfieldType, ',',
              self.get('Difficulty'), ',',
              self.TemperatureDay, ',',
              self.TemperatureNight,',',
              pCol,',',
              noise, ', ',
              t1, ', ',
              t2, ', ',
              t3, ', ',
              t4
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
        rand = drones.get('Random', None)
        if rand is None :
            return False
        rand = rand[0]
        group = rand.get('GroupName', None)
        if group != 'DroneBaseSetup':
            rand['GroupName'] = 'DroneBaseSetup'
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
            rnd = sp.get('Random', [])
            for item in rnd:
                minmax = item.get('DronesMinMax', [])
                mn = minmax[0]
                mx = minmax[1]
                drones += ((mx - mn) / 2) + mn

        poi = self.get('POIs')
        if poi is not None:
            for item in poi.get('Random', []):
                if item.get('DroneBaseSetup', None) is not None:
                    minmax = item.get('DronesMinMax', [])
                    mn = minmax[0]
                    mx = minmax[1]
                    drones += ((mx - mn) / 2) + mn

        return drones

    def getPOICount(self):
        # return the average number of generated POIs
        count = 0
        poi = self.get('POIs')
        if poi is not None:
            for item in poi.get('Random', []):
                if item.get('GroupName', None) is not None:
                    minmax = item.get('CountMinMax', [])
                    mn = minmax[0]
                    mx = minmax[1]
                    count += ((mx - mn) / 2) + mn

        return count

    def newTerrain(self):
        # create a new terrain for the playfield
        self.Terrain = {
            'Name': random.choice(terrainTypes),
            'PoleLevel': random.randint(28, 34),
            'NoiseStrength': random.uniform(0 , 0.8),
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
        self.props['PlanetType'] = self.Terrain['Name']

    def defaultBiome(self):
        #create minimal biome
        textures = random.sample(biomeTextures, 4)
        self.props['MainBiome'] = {
            'Textures' : [
                 [ textures[0],  1],
                 [ textures[1], 2],
                 [ textures[2], 0],
                 [ textures[3], 1]
             ]
        }

        self.props['Biome'] = [{
            'Altitude' : [0,10],
            'Slope' : [0, 2],
            'BiomeClusterData' : [{
                'Name': 'Water',
                'Id' : 1,
                'ClusterSize' : 1,
                'NbOfClusters' : 1,
                'Decorations' : [[ 'CoralBig01', 2]]
            }]
        }]

    def generatePOI(self):
        poi = {
            'Random' : [],
            'Fixed' : [],
            'FixedPlayerStart' : [
              {
                'Mode': 'Survival',
                'Spawn': 'EscapePod',
                'Armor': 'ArmorLight',
                'Items': [
                    "Pistol, 50Caliber:250, Medikit02:3, AntidotePills:3, EmergencyRations:4, Drill, Chainsaw, BioFuel:15, ConstructorSurvival, EnergyCell:5, OreScanner",
                    "Pistol, 50Caliber:150, Medikit02:2, AntidotePills:2, EmergencyRations:2, Drill, Chainsaw, BioFuel:10, ConstructorSurvival, EnergyCell:4, OreScanner",
                    "Pistol, 50Caliber:100, Medikit02:1, AntidotePills:1, EmergencyRations:1, Drill, Chainsaw, BioFuel:5, ConstructorSurvival, EnergyCell:3",
                    "#FreshStart: Pistol, 50Caliber:250, Drill, Chainsaw, BioFuel:15, ConstructorSurvival, OreScanner"
                    ]
              }
            ]
        }
        self.props['POIs'] = poi

