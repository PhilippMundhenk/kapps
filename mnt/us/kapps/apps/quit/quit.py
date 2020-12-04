from core.kapp import Kapp
from core.commands import Quit, Launcher
from core.httpResponse import HTTPResponse


class QuitApp(Kapp):
    name = "Quit"

    def homeCallback(self, kcommand):
        self.publish(Quit())
        return self.publish(Launcher())[0]

    def iconCallback(self, kcommand):
    	return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    print("register " + QuitApp.name)
    app = QuitApp(appID, appPath, ctx)
    return app
