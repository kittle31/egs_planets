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

    def parse(self, path):
        self.path = path
        with open(self.path, 'rb')  as fileHandle:
            string = fileHandle.read()
            string = string.replace(b"\t", b"")
            self.obj = yaml.load(string)

        self.TemperatureDay = self.obj.get('TemperatureDay', None)
        self.TemperatureNight = self.obj.get('TemperatureNight', None)
        self.playType = self.obj.get('PlayfieldType')
    def get(self, key):
        return self.obj.get(key, None)

    def report(self):
        print(self.playfieldName, ',' ,self.playType, ',', self.get('Difficulty'), ',',self.TemperatureDay, self.TemperatureNight)