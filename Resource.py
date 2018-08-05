import random

resourceT1 = ['IronResource', 'CopperResource', 'SiliconResource', 'PromethiumResource']
resourceT2 = ['CobaltResource','NeodymiumResource','MagnesiumResource',]
resourceT3 = ['SathiumResource','ErestrumResource','ZascosiumResource']
resourceSpecial = ['PentaxidResource', 'GoldResource']
ignoreList = ['GoldResource', 'PentaxidResource']

def intFloor(start, end, floor) :
    value = random.randint(start, end)
    if value <= floor :
        value = floor
    return value

def uniformFloor(start, end, floor) :
    value = random.uniform(start, end)
    if value <= floor :
        value = floor
    return value

class PlanetResource() :
    def __init__(self):
        self.Name = None
        self.CountMinMax= [1, 0]
        self.SizeMinMax= [0, 0]
        self.DepthMinMax= [0, 0]
        self.DroneProb= uniformFloor(-0.1, 1, 0)

    def random(self):
        #random values for this resource
        self.CountMinMax[0] = random.randint(1,5)
        inc = random.randint(0, 10)
        self.CountMinMax[1] = self.CountMinMax[0]+inc

        self.SizeMinMax[0] = random.randint(5,10)
        inc = random.randint(0,5)
        self.SizeMinMax[1] = self.SizeMinMax[0]+inc

        self.DepthMinMax[0] = intFloor(-1, 3, 0)
        inc = intFloor(-2, 4, 0)
        self.DepthMinMax[1] = self.SizeMinMax[0]+inc

    @classmethod
    def randomList(cls):
        resList = []
        resList.extend(cls.randomT1())
        resList.extend(cls.randomT2())
        resList.extend(cls.randomT3())
        resList.extend(cls.randomSpecial())
        return resList

    @classmethod
    def parse(cls, value):
        #value will be a list of instances
        result = []
        if value is None :
            return result
        for item in value :
            obj = PlanetResource()
            for key in item :
                setattr(obj, key, item[key])
            result.append(obj)
        return result

    @classmethod
    def instanceFromNames(cls, col):
        ress = []
        for item in col :
            res = PlanetResource()
            res.Name = item
            res.random()
            ress.append(res)

        return ress

    @classmethod
    def randomFromList(cls, list, emptyCutoff, missingCutoff, tier):
        #random list of resources
        if emptyCutoff > 0 and random.randint(1,100) <= emptyCutoff :
            # 50% chance of no res
            return []
        resList = list[:]
        if random.randint(1,100) <= missingCutoff :
            missing = random.choice(list)
            resList.remove(missing)
        res = PlanetResource.instanceFromNames(resList)
        for item in res :
            item.DroneProb += (tier / 10)
            if item.DroneProb > 1 :
                item.DroneProb = 1
        return res

    @classmethod
    def randomT1(cls):
        # random selection of T1 resources
        return PlanetResource.randomFromList(resourceT1, 0, 20, 1)

        # resList = resourceT1[:]
        # if random.randint(1,10) <= 2 :
        #     # 20% chance to drop 1 resource
        #     missing = random.choice(resourceT1)
        #     resList.remove(missing)
        #
        # return PlanetResource.instanceFromNames(resList, 1)

    @classmethod
    def randomT2(cls):
        #random list of T2 resources
        return PlanetResource.randomFromList(resourceT2, 50, 40, 2)

        # if random.randint(1,10) <= 5 :
        #     # 50% chance of no res
        #     return []
        # resList = resourceT2[:]
        # if random.randint(1,10) <= 4 :
        #     missing = random.choice(resourceT2)
        #     resList.remove(missing)
        # return PlanetResource.instanceFromNames(resList, 2)

    @classmethod
    def randomT3(cls):
        #random list of T3 resources
        return PlanetResource.randomFromList(resourceT3, 75, 30, 3)

        # if random.randint(1,100) <= 75 :
        #     # 75% chance of no res
        #     return []
        # resList = resourceT3[:]
        # if random.randint(1,10) <= 4 :
        #     missing = random.choice(resourceT3)
        #     resList.remove(missing)
        # return PlanetResource.instanceFromNames(resList, 3)

    @classmethod
    def randomSpecial(cls):
        #random list of special resources
        return PlanetResource.randomFromList(resourceSpecial, 80, 40, 4)
        # if random.randint(1,100) <= 80 :
        #     # 80 chance of no res
        #     return []
        # resList = resourceSpecial[:]
        # if random.randint(1,10) <= 4 :
        #     missing = random.choice(resourceSpecial)
        #     resList.remove(missing)
        # return PlanetResource.instanceFromNames(resList, 4)

    def makeMeteor(self):
        if self.Name in ignoreList :
            return None
        if random.uniform(0,1) <= 0.15 :
            #15% chance of no meteor
            return None

        m = MeteorResource()
        m.Name = self.Name
        m.random()
        return m

class MeteorResource :
    def __init__(self):
        self.Name = None
        self.Threshold = 0
        self.Amount = 0

    def random(self):
        self.Threshold = uniformFloor(0 ,1, 0.4)
        self.Amount = uniformFloor(-0.1, 1, 0.1)

    @classmethod
    def parse(self, value):
        #value will be a list of instances
        result = []
        if value is None :
            return None
        for item in value :
            obj = MeteorResource()
            for key in item :
                setattr(obj, key, item[key])
            result.append(obj)
        return result
