from core.kapp import Kapp
from core.commands import Quit


class QuitApp(Kapp):
    name = "Quit"

    def homeCallback(self):
        self.publish(Quit())
        return {"code": 301, "headers": [['Location', "/"]]}

    def iconCallback(self):
        return {"code": 200, "content": self.getRes("icon.png")}


def register(appID, appPath, ctx):
    print("register " + QuitApp.name)
    app = QuitApp(appID, appPath, ctx)
    return app
