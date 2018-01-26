import random

resourceT1 = ['IronResource', 'CopperResource', 'SiliconResource', 'PromethiumResource']
resourceT2 = ['CobaltResource','NeodymiumResource','MagnesiumResource',]
resourceT3 = ['SathiumResource','ErestrumResource','ZascosiumResource']
resourceSpecial = ['PentaxidResource', 'GoldResource']

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
    def randomT1(cls):
        # random selection of T1 resources
        resList = resourceT1[:]
        if random.randint(1,10) <= 2 :
            # 20% chance to drop 1 resource
            missing = random.choice(resourceT1)
            resList.remove(missing)

        return PlanetResource.instanceFromNames(resList)

    @classmethod
    def randomT2(cls):
        #random list of T2 resources
        if random.randint(1,10) <= 5 :
            # 50% chance of no T2 res
            return []
        resList = resourceT2[:]
        if random.randint(1,10) <= 4 :
            missing = random.choice(resourceT2)
            resList.remove(missing)
        return PlanetResource.instanceFromNames(resList)

    @classmethod
    def randomT3(cls):
        #random list of T2 resources
        if random.randint(1,100) <= 75 :
            # 75% chance of no T2 res
            return []
        resList = resourceT3[:]
        if random.randint(1,10) <= 4 :
            missing = random.choice(resourceT3)
            resList.remove(missing)
        return PlanetResource.instanceFromNames(resList)

    @classmethod
    def randomSpecial(cls):
        #random list of T2 resources
        if random.randint(1,100) <= 80 :
            # 80 chance of no res
            return []
        resList = resourceSpecial[:]
        if random.randint(1,10) <= 4 :
            missing = random.choice(resourceSpecial)
            resList.remove(missing)
        return PlanetResource.instanceFromNames(resList)


class MeteorResource :
    def __init__(self):
        self.Name = None
        self.Threshold = 0
        self.Amount = 0

    @classmethod
    def random(cls, tier):
        res = MeteorResource()
        if tier == 1 :
            res.Name = random.choice(resourceT1)
        if tier == 2 :
            res.Name = random.choice(resourceT2)
        if tier == 3 :
            res.Name = random.choice(resourceT3)
        res.Threshold = random.uniform(0.1, 0.5)
        res.Amount = random.uniform(0.1, 0.5)
