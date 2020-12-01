from core.kapp import Kapp


class Settings(Kapp):
    name = "Settings"

    def homeCallback(self):
        return {"code": 200, "content": self.getRes("list.html")}

    def iconCallback(self):
        return {"code": 200, "content": self.getRes("icon.png")}


def register(appID, appPath, ctx):
    print("register " + Settings.name)
    return Settings(appID, appPath, ctx)
