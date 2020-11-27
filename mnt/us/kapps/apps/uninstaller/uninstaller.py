import shutil


class Kapp():
    icon = "res/icon.png"
    name = "Uninstaller"

    def __init__(self, appID, appPath, ctx):
        self.appID = appID
        self.ctx = ctx
        self.appPath = appPath

    def getAppPythonPath(self):
        return self.appPath

    def getAppFSPath(self):
        return self.appPath.replace(".", "/") + "/"

    def urlToAppPath(self, url):
        return url.replace(self.getAppURL(), self.getAppFSPath())

    def getAppURL(self):
        return "/apps/" + str(self.appID)

    def getRes(self, path):
        with open(path.replace(self.getAppURL(), self.getAppFSPath()), 'r') as file:
            return file.read()

    def handleGet(self, path):
        if "/res" in path:
            # app resource requested
            return {"code": 200, "content": self.getRes(self.urlToAppPath(path))}
        elif path.startswith(self.getAppURL() + "/delete"):
            # format: /apps/<appID>/delete/<appName>
            appID = path.split(
                self.getAppURL() + "/delete")[1].replace("/", "", 1)

            app = self.ctx.getAppByIDString(appID)
            self.ctx.removeAppByIDString(appID)
            shutil.rmtree("/mnt/us/kapps/apps/" + app.name)

            return {"code": 301, "headers": [['Location', self.getAppURL()]]}
        elif path == self.getAppURL():
            # app is started

            text = ""

            for a in self.ctx.getApps():
                text = text + "<tr><td><a href=\"" + self.getAppURL() + \
                    "/delete/" + str(a) + "\"><h3>" + \
                    self.ctx.getApps()[a].name + "</h3></a></td></tr>"

            with open(self.urlToAppPath(path) + '/res/list.html', 'r') as file:
                return {"code": 200, "content": file.read().replace("$APPS$", text)}
        else:
            return {"code": 404, "content": "<html><h1>Not Found</h1></html>"}


def register(appID, appPath, ctx):
    print("register TestApp")
    return Kapp(appID, appPath, ctx)
