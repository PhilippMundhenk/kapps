class Kapp():
    def __init__(self, appID, appPath, ctx):
        self.appID = appID
        self.appPath = appPath
        self.ctx = ctx

    def getAppPythonPath(self):
        return self.appPath

    def getAppFSPath(self):
        return self.appPath.replace(".", "/") + "/"

    def getAppURL(self):
        return "/apps/" + str(self.appID)

    def urlToAppPath(self, url):
        return url.replace(self.getAppURL(), self.getAppFSPath())

    def getRes(self, path):
        with open(path, 'r') as file:
            return file.read()

    def subscribe(self, kcommand, callback):
        self.ctx.subscribe(kcommand, callback, self)

    def publish(self, kcommand):
        self.ctx.publish(kcommand)
