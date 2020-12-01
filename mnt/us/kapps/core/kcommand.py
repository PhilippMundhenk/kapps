class KcommandParam(object):
    paramEqual = "===:==="

    def __init__(self, key=None, value=None, string=None):
        if key is not None:
            self.key = key
            if value is not None:
                self.value = value
            else:
                self.value = None
        elif string is not None:
            self.fromString(string)

    def toString(self):
        paramString = ""
        paramString = paramString + "/" + self.key
        if self.value is not None:
            paramString = paramString + self.paramEqual + self.value

        return paramString

    def fromString(self, string):
        parts = string.split(self.paramEqual)
        self.key = parts[0]
        if len(parts) > 1:
            self.value = parts[1]


class Kcommand(object):
    def __init__(self, name, commandID, params=None):
        self.name = name
        self.commandID = commandID
        self.params = params

    def hash(self):
        return self.name + "." + self.commandID

    def toURL(self):
        paramString = ""
        if self.params is not None:
            for p in self.params:
                paramString = paramString + p.toString()

        return "/apps/" + self.hash() + paramString + "/"
