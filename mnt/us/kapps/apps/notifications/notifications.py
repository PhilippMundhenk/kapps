from core.kapp import Kapp, Home
from core.Kcommand import Kcommand, KcommandParam
import uuid


class Notify(Kcommand):
    def __init__(self, params=None):
        super(Notify, self).__init__(
            "Notify", "kapps-notification-command-hash", params=params)


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


class Notifications(Kapp):
    name = "Notifications"
    notifications = dict()

    def dismissCallback(self, params):
        for p in params:
            if p.key == "notifID":
                self.notifications.pop(p.value)

        return {"code": 301, "headers": [['Location', Home(self.homeHash).toURL()]]}

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
            text = text + "<tr style=\"border: solid; border-width: 1px 0;\">" + "<td>" + self.notifications[n].title + "<br />" + \
                self.notifications[n].message + "</td>" + "<td></td>" + "<td><a href=\"" + \
                DismissNotification([p]).toURL() + \
                '" class="button">Dismiss</a></td></tr>'

        content = self.getRes("list.html").replace("$NOTIFS$", text)
        return {"code": 200, "content": content}

    def iconCallback(self):
        return {"code": 200, "content": self.getRes("icon.png")}


def register(appID, appPath, ctx):
    print("register " + Notifications.name)
    app = Notifications(appID, appPath, ctx)
    app.subscribe(Notify(), app.notificationCallback)
    return app
