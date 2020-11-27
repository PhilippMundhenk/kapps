import os
import json
import urllib2
import ssl
import shutil


class Kapp():
    icon = "res/icon.png"
    name = "Installer"

    def __init__(self, appID, appPath, ctx):
        self.appID = appID
        self.appPath = appPath
        self.ctx = ctx

    def getAppPythonPath(self):
        return self.appPath

    def getAppFSPath(self):
        return self.appPath.replace(".", "/") + "/"

    def getAppURL(self):
        return "/apps/" + str(self.appID)

    def urlToAppPath(self, url):
        return url.replace(self.getAppURL(), self.getAppFSPath())

    def getRes(self, path):
        with open(path, 'r') as file:
            return file.read()

    def handleGet(self, path):
        if "/res" in path:
            # app resource requested
            return {"code": 200, "content": self.getRes(self.urlToAppPath(path))}
        if path.startswith(self.getAppURL() + "/download"):
            print("download triggered")

            # format: /apps/<appID>/download/<appName>
            appName = path.split(
                self.getAppURL() + "/download")[1].replace("/", "", 1)

            # Download list of available apps:
            request = urllib2.Request(
                'https://raw.githubusercontent.com/PhilippMundhenk/kapps-list/main/list')
            response = urllib2.urlopen(
                request, context=ssl._create_unverified_context())
            listFile = response.read().decode('utf-8')
            parsed = json.loads(listFile)

            tmpDir = "/mnt/us/kapps/tmp/"

            # download selected app:
            try:
                os.mkdir(tmpDir)
            except OSError:
                pass

            for a in parsed["apps"]:
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
                        shutil.rmtree("/mnt/us/kapps/apps/" +
                                      os.path.basename(folder))
                        # if this is successful, app was installed before, needs to be unregistered:
                        self.ctx.removeApp(self.ctx.getAppByPythonPath(
                            "apps." + os.path.basename(folder)))
                    except OSError:
                        pass
                    shutil.move(folder, "/mnt/us/kapps/apps")
                    os.remove(tmpDir + a["name"] + ".kapp")
                    shutil.rmtree(tmpPath)

                    self.ctx.scanApps()

            # TODO: redirect to app install screen
            return {"code": 301, "headers": [['Location', self.getAppURL()]]}
        elif path == self.getAppURL():
            # app is started

            text = ""

            # TODO: This should be fixed. Make sure cert is verified
            request = urllib2.Request(
                'https://raw.githubusercontent.com/PhilippMundhenk/kapps-list/main/list')
            response = urllib2.urlopen(
                request, context=ssl._create_unverified_context())
            listFile = response.read().decode('utf-8')
            parsed = json.loads(listFile)

            for a in parsed["apps"]:
                text = text + "<tr><td><a href=\"" + self.getAppURL() + \
                    "/download/" + a["name"] + "\"><h3>" + \
                    a["name"] + "</h3></a></td></tr>"

            with open(self.urlToAppPath(path) + '/res/list.html', 'r') as file:
                return {"code": 200, "content": file.read().replace("$APPS$", text)}
        else:
            return {"code": 404, "content": "<html><h1>Not Found</h1></html>"}


def register(appID, appPath, ctx):
    print("register Installer")
    return Kapp(appID, appPath, ctx)
