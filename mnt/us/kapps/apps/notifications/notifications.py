from core.kapp import Kapp
from core.Kcommand import Kcommand
from core.commands import Notify, Launcher
import uuid
from datetime import datetime
from core.httpResponse import HTTPResponse


class DismissNotification(Kcommand):
    dismissHash = str(uuid.uuid4())
    
    def __init__(self):
        super(DismissNotification, self).__init__(
            "DismissNotification", self.dismissHash)


class Notification():
    def __init__(self, title, message):
        self.title = title
        self.id = uuid.uuid4()
        self.message = message
        self.time = datetime.now()


class Notifications(Kapp):
    name = "Notifications"
    notifications = dict()

    def dismissCallback(self, kcommand):
        notifID = kcommand.getParam("notifID")
        print("notifID=" + notifID)
        print("self.notifications = " + str(self.notifications))
        self.notifications.pop(notifID)

        if len(self.notifications) == 0:
            return self.publish(Launcher())[0]
        else:
            ret = self.publish(self.getHomeCommand())
            return ret[0]

    def notificationCallback(self, kcommand):
        n = Notification(kcommand.getParam("title"),
                         kcommand.getParam("message"))
        self.notifications[str(n.id)] = n
        return None

    def homeCallback(self, kcommand):
        text = ""
        for n in self.notifications:
            text = text + "<tr style=\"border: solid; border-width: 1px 0;\">" + "<td>" + \
                "<b>" + self.notifications[n].title + "</b><br />" + \
                self.notifications[n].message + "<br/>" + \
                "<p style=\"font-size:15px;\">" + self.notifications[n].time.strftime("%H:%M") + "</p>" + \
                "</td>" + \
                "<td></td>" + "<td><a href=\"" + \
                DismissNotification().setParam("notifID", str(n)).toURL() + \
                '" class="button">Dismiss</a></td></tr>'

        content = self.getRes("list.html").replace("$NOTIFS$", text)
        return HTTPResponse(content=content)

    def iconCallback(self, kcommand):
        if len(self.notifications) > 0:
            return HTTPResponse(content=self.getRes("iconNewNotif.png"))
        else:
            return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    print("register " + Notifications.name)
    app = Notifications(appID, appPath, ctx)
    app.subscribe(Notify(), app.notificationCallback)
    app.subscribe(DismissNotification(), app.dismissCallback)
    return app
