import re


class Kcommand(object):
    paramEqual = "===:==="

    def __init__(self, name, commandID):
        self.name = name
        self.commandID = commandID
        self.params = dict()

    def setParam(self, name, param):
        return self.setParameter(name, param)

    def getParam(self, name):
        return self.getParameter(name)

    def setParameter(self, name, param):
        self.params[name] = param
        return self

    def getParameter(self, name):
        return self.params[name]

    def commandIDfromHash(self, hashString):
        self.commandID = hashString.split(".")[1]

    def hash(self):
        return self.name + "." + self.commandID

    def toURL(self):
        paramString = ""
        for p in self.params:
            paramString = paramString + "/" + \
                p.replace("/", "//") + self.paramEqual + \
                str(self.params[p]).replace("/", "//")

        return "/apps/" + self.hash() + paramString

    def paramsFromString(self, string):
        self.paramCount = 0
        self.params = dict()

        # split for single / but not //, ignore initial /:
        paramList = re.split("(?<!/)/(?!/)", string[1:])
        for p in paramList:
            parts = p.split(self.paramEqual)
            val = None
            if len(parts) > 1:
                val = parts[1].replace("//", "/")

            self.params[parts[0].replace("//", "/")] = val
            self.paramCount = self.paramCount + 1
