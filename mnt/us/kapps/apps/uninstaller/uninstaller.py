import shutil
from core.kapp import Kapp
from core.Kcommand import Kcommand
import uuid
from core.commands import Launcher, Notify
from core.httpResponse import HTTPResponse


class Uninstall(Kcommand):
    uninstallHash = str(uuid.uuid4())

    def __init__(self):
        super(Uninstall, self).__init__(
            "Uninstall", self.uninstallHash)


class Uninstaller(Kapp):
    name = "Uninstaller"

    def uninstallCallback(self, kcommand):
        appID = kcommand.getParam("appID")
        app = self.ctx.getAppByIDString(appID)
        self.ctx.removeAppByIDString(appID)
        shutil.rmtree(self.ctx.getBasePath() + "/apps/" + app.name)
        self.publish(Notify().setParam("title", "Uninstaller").setParam(
            "message", "App " + app.name + " uninstalled"))

        return self.publish(Launcher())[0]

    def homeCallback(self, kcommand):
        # app is started
        text = ""

        for appID, a in self.ctx.getSortedApps():
            if not self.ctx.isSystemApp(a.getAppPythonPath()):
                text = text + "<tr><td><h3>" + \
                    a.name + '</h3></td><td></td>' + \
                    '<td><a href="' + Uninstall().setParam("appID", appID).toURL() + \
                    '" class="button">uninstall</a>' + \
                    '</td></tr>'

        content = self.getRes("list.html").replace("$APPS$", text)
        return HTTPResponse(content=content)

    def iconCallback(self, kcommand):
        return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    print("register " + Uninstaller.name)
    app = Uninstaller(appID, appPath, ctx)
    app.subscribe(Uninstall(), app.uninstallCallback)
    return app
