from core.kapp import Kapp
from core.kcommand import Kcommand


class Ping(Kcommand):
    def __init__(self):
        super(Ping, self).__init__("Ping", "df7f0f6a-c920-48ad-b8d2-ff79cc251165")


class Settings(Kapp):
    icon = "res/icon.png"
    name = "Settings"

    def handleGet(self, path):
        if "/res" in path:
            # app resource requested
            return {"code": 200, "content": self.getRes(self.urlToAppPath(path))}
        elif path.startswith(self.getAppURL()):
            # app is started

            self.publish(Ping())

            # TODO: replace "$SETTINGS$" with actual settings
            with open(self.getAppFSPath() + '/res/list.html', 'r') as file:
                return {"code": 200, "content": file.read()}
        else:
            return {"code": 404, "content": '<html><head><meta http-equiv = "refresh" content = "2; url = /" /></head><h1 align="center">Error!</h1></html>'}


def register(appID, appPath, ctx):
    print("register " + Settings.name)
    return Settings(appID, appPath, ctx)
