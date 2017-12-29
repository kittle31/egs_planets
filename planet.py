import math


class SectorPlanet :
    def __init__(self):
        self.location = [0,0,0]
        self.playfields = []
        self.color = [0,0,0]
        self.orbitLine = False
        self.icon = None
        self.deny = []
        self.allow = []
        self.name = '<empty>'
        self.diff = None

    @staticmethod
    def loadFrom(yml, planetDb):
        #create from yaml object
        pl = SectorPlanet()
        pl.location = yml.get('Coordinates')
        pl.color = yml.get('Color')
        pl.icon = yml.get('Icon', None)
        pl.allow = yml.get('Allow', [])
        pl.deny = yml.get('Deny', [])
        for item in yml.get('Playfields', []) :
            pl.playfields.append(Planet.loadFrom(item, planetDb ))
        if len(pl.playfields) > 0 :
            pl.name = pl.playfields[0].name

        return pl

    def __repr__(self):
        if len(self.playfields) == 0 :
            return '<empty>'
        else :
            return self.playfields[0].name

    def write(self, file):
        file.write('- Coordinates: '+str(self.location)+'\n')
        file.write('  Color: '+str(self.color)+'\n')
        if self.icon is not None :
            file.write('  Icon: '+str(self.icon)+'\n')
        if self.allow is not None :
            file.write('  Allow: '+str(self.allow)+'\n')
        if self.deny is not None :
            file.write('  Deny: '+str(self.deny)+'\n')
        file.write('  Playfields:\n')
        for item in self.playfields :
            file.write('  - ')
            item.write(file)

    def getDiff(self):
        if self.diff is not None :
            return self.diff

        diff = 0
        if len(self.playfields) == 0 :
            return 0

        for item in self.playfields :
            diff += item.diff
        self.diff = math.floor(diff / len(self.playfields))
        return self.diff

    def distanceTo(self, otherSector):
        x1=self.location[0]
        y1=self.location[1]
        z1=self.location[2]
        x2=otherSector.location[0]
        y2=otherSector.location[1]
        z2=otherSector.location[2]
        xs = (x2-x1)**2
        ys = (y2-y1)**2
        zs = (z2-z1)**2
        return math.sqrt(xs+ys+zs)

class Planet :
    def __init__(self):
        self.location = [0,0,0]
        self.name = ''
        self.templateName = ''
        self.startString = None

    @staticmethod
    def loadFrom(yml, planetDb):
        p = Planet()
        p.location = yml[0]
        p.name = yml[1]
        p.templateName = yml[2]
        if len(yml) > 3 :
            p.startString = yml[3]

        if planetDb is not None :
           planet = planetDb.get(p.templateName, None)
           if planet is not None :
               p.diff = planet.getDiff()
        return p

    def __repr__(self):
        return self.name

    def write(self, file):
        file.write('[')
        file.write("'"+str(self.location)+"'")
        file.write(', '+self.name)
        file.write(', '+self.templateName)
        if self.startString is not None :
            file.write(", '"+self.startString+"'")
        file.write(']\n')
