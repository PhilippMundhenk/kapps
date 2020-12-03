from core.kapp import Kapp
from core.httpResponse import HTTPResponse


class Settings(Kapp):
    name = "Settings"

    def homeCallback(self):
        return HTTPResponse(content=self.getRes("list.html"))

    def iconCallback(self):
        return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    print("register " + Settings.name)
    return Settings(appID, appPath, ctx)
