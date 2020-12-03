from core.kapp import Kapp
from core.commands import Quit, Launcher


class QuitApp(Kapp):
    name = "Quit"

    def homeCallback(self):
        self.publish(Quit())
        return self.publish(Launcher())[0]

    def iconCallback(self):
        return {"code": 200, "content": self.getRes("icon.png")}


def register(appID, appPath, ctx):
    print("register " + QuitApp.name)
    app = QuitApp(appID, appPath, ctx)
    return app
