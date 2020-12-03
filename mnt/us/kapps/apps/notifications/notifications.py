from core.kapp import Kapp, Home
from core.Kcommand import Kcommand, KcommandParam
from core.commands import Notify, Launcher
import uuid
from datetime import datetime


class DismissNotification(Kcommand):
    dismissHash = str(uuid.uuid4())

    def __init__(self, params=None):
        super(DismissNotification, self).__init__(
            "DismissNotification", self.dismissHash, params=params)


class Notification():
    def __init__(self, title):
        self.title = title
        self.id = uuid.uuid4()
        self.message = ""
        self.time = datetime.now()


class Notifications(Kapp):
    name = "Notifications"
    notifications = dict()

    def dismissCallback(self, params):
        for p in params:
            if p.key == "notifID":
                self.notifications.pop(p.value)

        if len(self.notifications) == 0:
            return self.publish(Launcher())[0]
        else:
            return self.publish(Home(self.homeHash))[0]

    def notificationCallback(self, params):
        n = None
        for p in params:
            if p.key == "title":
                n = Notification(p.value)
            elif p.key == "message":
                n.message = p.value

        self.notifications[str(n.id)] = n
        return None

    def homeCallback(self):
        self.subscribe(DismissNotification(), self.dismissCallback)

        text = ""
        for n in self.notifications:
            p = KcommandParam(key="notifID", value=str(n))
            text = text + "<tr style=\"border: solid; border-width: 1px 0;\">" + "<td>" + \
                "<b>" + self.notifications[n].title + "</b><br />" + \
                self.notifications[n].message + "<br/>" + \
                "<p style=\"font-size:15px;\">" + self.notifications[n].time.strftime("%H:%M") + "</p>" + \
                "</td>" + \
                "<td></td>" + "<td><a href=\"" + \
                DismissNotification([p]).toURL() + \
                '" class="button">Dismiss</a></td></tr>'

        content = self.getRes("list.html").replace("$NOTIFS$", text)
        return {"code": 200, "content": content}

    def iconCallback(self):
        if len(self.notifications) > 0:
            return {"code": 200, "content": self.getRes("iconNewNotif.png")}
        else:
            return {"code": 200, "content": self.getRes("icon.png")}


def register(appID, appPath, ctx):
    print("register " + Notifications.name)
    app = Notifications(appID, appPath, ctx)
    app.subscribe(Notify(), app.notificationCallback)
    return app
