import shutil
from core.kapp import Kapp
from core.Kcommand import Kcommand, KcommandParam
import uuid
from core.commands import Launcher, Notify
from core.httpResponse import HTTPResponse


class Uninstall(Kcommand):
    uninstallHash = str(uuid.uuid4())

    def __init__(self, params=None):
        super(Uninstall, self).__init__(
            "Uninstall", self.uninstallHash, params=params)


class Uninstaller(Kapp):
    name = "Uninstaller"

    def uninstallCallback(self, params):
        for p in params:
            if p.key == "appID":
                appID = p.value

                app = self.ctx.getAppByIDString(appID)
                self.ctx.removeAppByIDString(appID)
                shutil.rmtree(self.ctx.getBasePath() + "/apps/" + app.name)

                title = KcommandParam(key="title", value="Uninstaller")
                message = KcommandParam(
                    key="message", value="App " + a["name"] + " uninstalled")
                self.publish(Notify([title, message]))

        return self.publish(Launcher())[0]

    def homeCallback(self):
        # app is started
        text = ""

        self.subscribe(Uninstall(), self.uninstallCallback)

        for appID, a in self.ctx.getSortedApps():
            if not self.ctx.isSystemApp(a.getAppPythonPath()):
                p = KcommandParam(key="appID", value=str(appID))
                print("Uninstall([p]).toURL()=" + Uninstall([p]).toURL())
                text = text + "<tr><td><h3>" + \
                    a.name + '</h3></td><td></td>' + \
                    '<td><a href="' + Uninstall([p]).toURL() + \
                    '" class="button">uninstall</a>' + \
                    '</td></tr>'

        content = self.getRes("list.html").replace("$APPS$", text)
        return HTTPResponse(content=content)

    def iconCallback(self):
        return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    print("register " + Uninstaller.name)
    return Uninstaller(appID, appPath, ctx)
