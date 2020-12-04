from core.kcommand import Kcommand
import uuid
from core.httpResponse import HTTPResponse


class Home(Kcommand):
    def __init__(self):
        super(Home, self).__init__(
            "Home", "kapps-home-command-hash")


class Icon(Kcommand):
    def __init__(self):
        super(Icon, self).__init__(
            "Icon", "kapps-icon-command-hash")


class Resource(Kcommand):
    def __init__(self):
        super(Resource, self).__init__(
            "Resource", "kapps-resource-command-hash")


class Kapp():
    def __init__(self, appID, appPath, ctx):
        self.appID = appID
        self.appPath = appPath
        self.ctx = ctx
        self.homeHash = str(uuid.uuid4())
        self.iconHash = str(uuid.uuid4())
        self.resourceHash = str(uuid.uuid4())

        h = Home()
        h.commandID = self.homeHash
        self.subscribe(h, self.homeCallback)
        i = Icon()
        i.commandID = self.iconHash
        self.subscribe(i, self.iconCallback)
        r = Resource()
        r.commandID = self.resourceHash
        self.subscribe(r, self.resourceCallback)

    def needsLauncherEntry(self):
        return True

    def getAppPythonPath(self):
        return self.appPath

    def getAppFSPath(self):
        return self.appPath.replace(".", "/") + "/"

    def urlToAppPath(self, url):
        return url.replace(self.getAppURL(), self.getAppFSPath())

    def getRes(self, path):
        with open(self.getAppFSPath() + "/res/" + path, 'r') as file:
            return file.read()

    def subscribe(self, kcommand, callback):
        self.ctx.subscribe(kcommand, callback, self)

    def publish(self, kcommand):
        return self.ctx.publish(kcommand)

    def homeCallback(self, kcommand):
        with open(self.ctx.getCorePath() + '/res/appHome.html', 'r') as file:
            return HTTPResponse(content=file.read().replace("$APPNAME$", self.name))

    def iconCallback(self, kcommand):
        with open(self.ctx.getCorePath() + '/res/appIcon.png', 'r') as file:
            return HTTPResponse(content=file.read())

    def resourceCallback(self, kcommand):
        return HTTPResponse(content=self.getRes(kcommand.getParameter("path")))

    def getHomeCommand(self):
        h = Home()
        h.commandID = self.homeHash
        return h

    def getIconCommand(self):
        i = Icon()
        i.commandID = self.iconHash
        return i
