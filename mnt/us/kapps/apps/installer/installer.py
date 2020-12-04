import os
import json
import urllib2
import ssl
import shutil
from core.kapp import Kapp
import uuid
from core.kcommand import Kcommand
from core.commands import Launcher, Notify
from core.httpResponse import HTTPResponse


class WaitScreen(Kcommand):
    waitScreenHash = str(uuid.uuid4())

    def __init__(self):
        super(WaitScreen, self).__init__(
            "WaitScreen", self.waitScreenHash)


class Install(Kcommand):
    installHash = str(uuid.uuid4())

    def __init__(self):
        super(Install, self).__init__(
            "Install", self.installHash)


class Installer(Kapp):
    name = "Installer"

    def iconCallback(self, kcommand):
        return HTTPResponse(content=self.getRes("icon.png"))

    def homeCallback(self, kcommand):
        # app is started
        text = ""

        # TODO: This should be fixed. Make sure cert is verified
        request = urllib2.Request(
            'https://raw.githubusercontent.com/PhilippMundhenk/kapps-list/main/list')
        response = urllib2.urlopen(
            request, context=ssl._create_unverified_context())
        listFile = response.read().decode('utf-8')
        self.availableApps = json.loads(listFile)

        text = text + '<tr><td colspan="3"><p style="font-size:25px;"><u>Repo github.com/PhilippMundhenk/kapps-list:</u></p></td></tr>'

        for a in self.availableApps["apps"]:
            text = text + "<tr><td><h3>" + \
                a["name"] + "</h3></td><td></td><td><a href=\"" + \
                WaitScreen().setParam("appName", a["name"]).toURL() + \
                '" class="button">(re-)install/update</a></td></tr>'

        content = self.getRes("list.html").replace("$APPS$", text)
        return HTTPResponse(content=content)

    def waitScreenCallback(self, kcommand):
        page = self.getRes("installing.html")
        page = page.replace("$APP$", kcommand.getParam("appName"))

        installCmd = Install()
        installCmd.params = kcommand.params

        page = page.replace("$URL$", installCmd.toURL())

        return HTTPResponse(content=page)

    def installCallback(self, kcommand):
        print("download triggered")

        appName = kcommand.getParam("appName")
        tmpDir = self.ctx.getBasePath() + "/tmp/"

        # download selected app:
        try:
            os.mkdir(tmpDir)
        except OSError:
            pass

        for a in self.availableApps["apps"]:
            if a["name"] == appName:
                with open(tmpDir + appName + '.kapp', 'wb') as f:
                    request = urllib2.Request(a["package"])
                    response = urllib2.urlopen(
                        request, context=ssl._create_unverified_context())
                    f.write(response.read())
                    f.close()

                tmpPath = tmpDir + a["name"]
                try:
                    shutil.rmtree(tmpPath)
                except OSError:
                    pass
                os.mkdir(tmpPath)
                command = "unzip " + tmpDir + appName + \
                    ".kapp -d " + tmpPath
                os.system(command)

                manifestFile = [os.path.join(dp, f) for dp, dn,
                                filenames in os.walk(tmpPath) for f in filenames if os.path.basename(f) == 'manifest.kapp'][0]
                with open(manifestFile) as f:
                    manifest = json.loads(f.read())
                    folder = os.path.dirname(
                        manifestFile) + "/" + manifest["app"]["folder"]

                try:
                    shutil.rmtree(self.ctx.getBasePath() + "/apps/" +
                                  os.path.basename(folder))
                    # if this is successful, app was installed before, needs to be unregistered:
                    self.ctx.removeApp(self.ctx.getAppByPythonPath(
                        "apps." + os.path.basename(folder)))
                except OSError:
                    pass
                shutil.move(folder, self.ctx.getBasePath() + "/apps")
                os.remove(tmpDir + a["name"] + ".kapp")
                shutil.rmtree(tmpPath)

                self.ctx.scanApps()

                self.publish(Notify().setParam("title", "Installer").setParam(
                    "message", "App " + a["name"] + " installed"))

        return self.publish(Launcher())[0]


def register(appID, appPath, ctx):
    print("register " + Installer.name)
    app = Installer(appID, appPath, ctx)
    app.subscribe(WaitScreen(), app.waitScreenCallback)
    app.subscribe(Install(), app.installCallback)
    return app
