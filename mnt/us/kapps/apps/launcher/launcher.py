from core.kapp import Kapp
from core.commands import Launcher
from core.httpResponse import HTTPResponse


class LauncherApp(Kapp):
    name = "Launcher"

    def needsLauncherEntry(self):
        return False

    def homeCallback(self, kcommand):
        self.publish(Launcher())
        return self.publish(Launcher())[0]

    def iconCallback(self, kcommand):
        return HTTPResponse(content=self.getRes("icon.png"))

    def launcherCallBack(self, kcommand):
        # TODO: Insert reading of apps here!
        text = "<tr>"
        cnt = 0
        for uuid, app in self.ctx.getSortedApps():
            if app.needsLauncherEntry():
                text = text + "<td>" + "<p align=\"center\"><a href=\"" + app.getHomeCommand().toURL() + "\"><img border=\"0\" src=\"" + app.getIconCommand().toURL() + "\"/><br/>" + \
                    app.name + "</a></p>" + "</td>"

                cnt = cnt + 1
                if cnt % 3 == 0:
                    text = text + "</tr><tr>"
        text = text + "</tr>"

        return HTTPResponse(content=self.getRes("launcher.html").replace("$APPS$", text))


def register(appID, appPath, ctx):
    print("register " + LauncherApp.name)
    app = LauncherApp(appID, appPath, ctx)
    app.subscribe(Launcher(), app.launcherCallBack)
    return app
