import os
import json
import urllib2
import ssl
import shutil
from core.kapp import Kapp
import uuid
from core.kcommand import Kcommand, KcommandParam


class WaitScreen(Kcommand):
    waitScreenHash = str(uuid.uuid4())

    def __init__(self, params=None):
        super(WaitScreen, self).__init__(
            "WaitScreen", self.waitScreenHash, params=params)


class Install(Kcommand):
    installHash = str(uuid.uuid4())

    def __init__(self, params=None):
        super(Install, self).__init__(
            "Install", self.installHash, params=params)


class Installer(Kapp):
    name = "Installer"

    def iconCallback(self):
        return {"code": 200, "content": self.getRes("icon.png")}

    def homeCallback(self):
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

        self.subscribe(WaitScreen(), self.waitScreenCallback)

        for a in self.availableApps["apps"]:
            p = KcommandParam(key="appName", value=a["name"])

            print("WaitScreen([p]).toURL()=" + WaitScreen([p]).toURL())
            text = text + "<tr><td><h3>" + \
                a["name"] + "</h3></td><td></td><td><a href=\"" + \
                WaitScreen([p]).toURL() + \
                '" class="button">(re-)install/update</a></td></tr>'

            print("text= " + text)

        content = self.getRes("list.html").replace("$APPS$", text)
        return {"code": 200, "content": content}

    def waitScreenCallback(self, params):
        # TODO: unsubscribe WaitScreen?
        page = self.getRes("installing.html")
        for p in params:
            if p.key == "appName":
                page = page.replace("$APP$", p.value)

                self.subscribe(Install(), self.installCallback)

                print("Install(params).toURL()=" + Install(params).toURL())
                # TODO: replace with install command!
                page = page.replace("$URL$", Install(params).toURL())

                return {"code": 200, "content": page}

        else:
            # TODO: Pythonize this!
            return {"code": 404, "content": '<html><head><meta http-equiv = "refresh" content = "2; url = /" /></head><h1 align="center">Error!</h1></html>'}

    def installCallback(self, params):
        # TODO: unsubscribe Install?
        print("download triggered")

        # format: /apps/<appID>/download/<appName>
        for p in params:
            if p.key == "appName":
                appName = p.value

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

        # TODO: Pythonize this!
        return {"code": 301, "headers": [['Location', "/"]]}


def register(appID, appPath, ctx):
    print("register " + Installer.name)
    return Installer(appID, appPath, ctx)
