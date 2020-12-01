from core.kapp import Kapp
from core.kcommand import Kcommand


class Ping(Kcommand):
    def __init__(self):
        super(Ping, self).__init__(
            "Ping", "df7f0f6a-c920-48ad-b8d2-ff79cc251165")


class TestApp(Kapp):
    name = "TestApp"

    def handlePing(self):
        print("Ping received")
        return "xyz"

    def homeCallback(self):
        self.publish(Ping())
        return {"code": 200, "content": self.getRes("testApp.html")}

    def iconCallback(self):
        return {"code": 200, "content": self.getRes("icon.png")}


def register(appID, appPath, ctx):
    print("register " + TestApp.name)
    app = TestApp(appID, appPath, ctx)
    app.subscribe(Ping(), app.handlePing)
    return app
