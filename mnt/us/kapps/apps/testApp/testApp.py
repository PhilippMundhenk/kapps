from core.kapp import Kapp
from core.kcommand import Kcommand


class Ping(Kcommand):
    def __init__(self):
        super(Ping, self).__init__(
            "Ping", "df7f0f6a-c920-48ad-b8d2-ff79cc251165")


class TestApp(Kapp):
    icon = "res/icon.png"
    name = "TestApp"

    def handlePing(self):
        print("Ping received")

    def handleGet(self, path):
        if "/res" in path:
            # app resource requested
            return {"code": 200, "content": self.getRes(self.urlToAppPath(path))}
        elif path.split(self.getAppURL())[1] == "":
            # app is started
            with open(self.getAppFSPath() + "/res/testApp.html", 'r') as file:
                return {"code": 200, "content": file.read()}
        else:
            return {"code": 404, "content": "<html><h1>Not Found</h1></html>"}


def register(appID, appPath, ctx):
    print("register " + TestApp.name)
    app = TestApp(appID, appPath, ctx)
    app.subscribe(Ping(), app.handlePing)
    return app
