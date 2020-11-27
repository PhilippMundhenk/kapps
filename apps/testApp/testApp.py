class Kapp():
    icon = "res/icon.png"
    name = "TestApp"

    def __init__(self, appID, appPath, ctx):
        self.appID = appID
        self.ctx = ctx
        self.appPath = appPath

    def getAppPythonPath(self):
        return self.appPath

    def getAppFSPath(self):
        return self.appPath.replace(".", "/") + "/"

    def getAppURL(self):
        return "/apps/" + str(self.appID)

    def getRes(self, path):
        with open(path.replace(self.getAppURL(), self.getAppFSPath()), 'r') as file:
            return file.read()

    def handleGet(self, path):
        if "/res" in path:
            # app resource requested
            return {"code": 200, "content": self.getRes(path)}
        elif path.split(appFolder)[1] == "":
            # app is started
            return {"code": 200, "content": "<html><h1>Alarm App</h1></html>"}
        else:
            return {"code": 404, "content": "<html><h1>Not Found</h1></html>"}


def register(appID, appPath, ctx):
    print("register TestApp")
    return Kapp(appID, appPath, ctx)
