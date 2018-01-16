import random

resourceT1 = ['IronResource', 'CopperResource','SiliconResource', 'PromethiumResource']
resourceT2 = ['CobaltResource','NeodymiumResource','MagnesiumResource',]
resourceT3 = ['SathiumResource','ErestrumResource','ZascosiumResource']

class PlanetResource :
    def __init__(self):
        self.Name = None
        self.CountMinMax= [1, 0]
        self.SizeMinMax= [0, 0]
        self.DepthMinMax= [0, 0]
        self.DroneProb= 0.0

    @classmethod
    def random(cls, tier):
        res = PlanetResource()
        res.CountMinMax[0] = 1
        res.CountMinMax[1] = random.randint(1,3)

        res.SizeMinMax[0] = random.randint(1,6)
        inc = random.randint(0,3)
        res.SizeMinMax[1] = res.SizeMinMax[0]+inc

        res.DepthMinMax[0] = random.randint(0,3)
        inc = random.randint(-2,4)
        if inc < 0 :
            inc = 0
        res.DepthMinMax[1] = res.SizeMinMax[0]+inc

        if tier == 1 :
            res.Name = random.choice(resourceT1)
        if tier == 2 :
            res.Name = random.choice(resourceT2)
        if tier == 3 :
            res.Name = random.choice(resourceT3)
        return res

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
