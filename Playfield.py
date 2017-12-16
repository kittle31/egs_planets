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
        print(self.playfieldName, ',' ,self.playType, ',', self.get('Difficulty'), ',', self.terrainType, ',', self.TemperatureDay, self.TemperatureNight)