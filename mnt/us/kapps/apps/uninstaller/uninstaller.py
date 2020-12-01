import shutil
from core.kapp import Kapp


class Uninstaller(Kapp):
    icon = "res/icon.png"
    name = "Uninstaller"

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

            for uuid, a in self.ctx.getSortedApps():
                if not self.ctx.isSystemApp(a.getAppPythonPath()):
                    text = text + "<tr><td><h3>" + \
                        a.name + '</h3></td><td></td>' + \
                        '<td><a href="' + self.getAppURL() + \
                        "/delete/" + str(uuid) + '" class="button">uninstall</a>' + \
                        '</td></tr>'

            with open(self.urlToAppPath(path) + '/res/list.html', 'r') as file:
                return {"code": 200, "content": file.read().replace("$APPS$", text)}
        else:
            return {"code": 404, "content": '<html><head><meta http-equiv = "refresh" content = "2; url = /" /></head><h1 align="center">Error!</h1></html>'}


def register(appID, appPath, ctx):
    print("register " + Uninstaller.name)
    return Uninstaller(appID, appPath, ctx)
