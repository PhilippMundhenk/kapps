from core.kcommand import Kcommand
import uuid


class Home(Kcommand):
    def __init__(self, classHash):
        super(Home, self).__init__(
            "Home", classHash)


class Icon(Kcommand):
    def __init__(self, classHash):
        super(Icon, self).__init__(
            "Icon", classHash)


class Resource(Kcommand):
    def __init__(self, classHash):
        super(Resource, self).__init__(
            "Resource", classHash)


class Kapp():
    def __init__(self, appID, appPath, ctx):
        self.appID = appID
        self.appPath = appPath
        self.ctx = ctx
        self.homeHash = str(uuid.uuid4())
        self.iconHash = str(uuid.uuid4())
        self.resourceHash = str(uuid.uuid4())

        self.subscribe(Home(self.homeHash), self.homeCallback)
        self.subscribe(Icon(self.iconHash), self.iconCallback)
        self.subscribe(Resource(self.resourceHash), self.resourceCallback)

    def getAppPythonPath(self):
        return self.appPath

    def getAppFSPath(self):
        return self.appPath.replace(".", "/") + "/"

    def getAppURL(self):
        return "/apps/" + str(self.appID)

    def urlToAppPath(self, url):
        return url.replace(self.getAppURL(), self.getAppFSPath())

    def getRes(self, path):
        with open(self.getAppFSPath() + "/res/" + path, 'r') as file:
            return file.read()

    def subscribe(self, kcommand, callback):
        self.ctx.subscribe(kcommand, callback, self)

    def publish(self, kcommand):
        return self.ctx.publish(kcommand)

    def homeCallback(self):
        with open(self.ctx.getCorePath() + '/res/appHome.html', 'r') as file:
            return {"code": 200, "content": file.read().replace("$APPNAME$", self.name)}

    def iconCallback(self):
        with open(self.ctx.getCorePath() + '/res/appIcon.png', 'r') as file:
            return {"code": 200, "content": file.read()}

    def resourceCallback(self, param):
        return {"code": 200, "content": self.getRes(param)}

    def getHomeCommand(self):
        return Home(self.homeHash)

    def getIconCommand(self):
        return Icon(self.iconHash)
