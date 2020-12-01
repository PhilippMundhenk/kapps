class Kcommand(object):
    def __init__(self, name, commandID):
        self.name = name
        self.commandID = commandID

    def hash(self):
        return self.name + "." + self.commandID
