from core.kapp import Kapp
from core.httpResponse import HTTPResponse


class Settings(Kapp):
    name = "Settings"

    def homeCallback(self, kcommand):
        return HTTPResponse(content=self.getRes("list.html"))

    def iconCallback(self, kcommand):
        return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    print("register " + Settings.name)
    return Settings(appID, appPath, ctx)
