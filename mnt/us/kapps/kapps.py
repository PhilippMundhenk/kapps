from BaseHTTPServer import HTTPServer
from core.httpRESTHandler import HTTPRESTHandler
import importlib
import pkgutil
import uuid
from subprocess import call
import apps
import os
import shutil
from core.commands import *
import traceback


basePath = "/mnt/us/kapps/"
corePath = basePath + "/core/"
appPath = basePath + "/apps/"


class Core():
    systemApps = ["apps.installer", "apps.uninstaller",
                  "apps.settings", "apps.quit"]
    apps = {}
    subscriptions = {}
    commandRegistry = {}

    def import_submodules(self, package, recursive=True):
        """ Import all submodules of a module, recursively,
            including subpackages

        :param package: package (name or actual module)
        :type package: str | module
        :rtype: dict[str, types.ModuleType]
        """
        if isinstance(package, str):
            package = importlib.import_module(package)
        results = {}
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                results.update(self.import_submodules(full_name))
        return results

    def scanApps(self):
        AllApps = self.import_submodules(apps)

        for name in AllApps:
            print("found " + name)
            alreadyRegistered = False
            for a in self.apps:
                if name.startswith(self.apps[a].getAppPythonPath()):
                    print("app " + name + " is already registered")
                    alreadyRegistered = True

            if not alreadyRegistered:
                try:
                    register = getattr(AllApps[name], "register")
                    appID = uuid.uuid4()
                    print("registering " + name + "...")
                    app = register(appID, name.rsplit(".", 1)[0], self)
                    print(name + " registered")
                    self.apps[appID] = app
                    print("list of apps=" + str(self.apps))
                except AttributeError as e:
                    print("Error registering app: ")
                    print(e)

    def removeAppByID(self, appID):
        self.apps.pop(appID)

    def isSystemApp(self, pythonPath):
        if pythonPath in self.systemApps:
            return True
        else:
            return False

    def removeAppByIDString(self, appID):
        try:
            self.apps.pop(uuid.UUID(appID))
        except KeyError:
            print("Don't have " + appID + ", can offer:")
            for a in self.apps:
                print(a)

    def removeApp(self, app):
        for a in self.apps:
            if self.apps[a] == app:
                self.apps.pop(a)
                break

    def getApps(self):
        return self.apps

    def getSortedApps(self):
        return sorted(self.getApps().items(), key=lambda x: x[1].name)

    def getAppByIDString(self, idString):
        return self.apps[uuid.UUID(idString)]

    def getAppByID(self, id):
        return self.apps[id]

    def getAppByPythonPath(self, path):
        for a in self.apps:
            if self.apps[a].getAppPythonPath() == path:
                return self.apps[a]

    def flushScreen(self, kcommand):
        cmd = "echo 1 > /sys/devices/platform/mxc_epdc_fb/mxc_epdc_update"
        os.system(cmd)

    def getKcommand(self, kcommandHash):
        cmd = self.commandRegistry[kcommandHash]()
        cmd.commandIDfromHash(kcommandHash)
        return cmd

    def subscribe(self, kcommand, callback, subscriber):
        print("subscription received for " + kcommand.hash())
        if kcommand.hash() in self.subscriptions:
            self.subscriptions[kcommand.hash()].append(callback)
        else:
            self.subscriptions[kcommand.hash()] = [callback]

        if kcommand.hash() not in self.commandRegistry:
            self.commandRegistry[kcommand.hash()] = type(kcommand)

    def publish(self, kcommand):
        try:
            print("publish with kcommand=" + str(kcommand) +
                  " and kcommand.hash()=" + kcommand.hash())
            if kcommand.hash() in self.subscriptions:
                returns = []
                for callback in self.subscriptions[kcommand.hash()]:
                    resp = callback(kcommand)
                    returns.append(resp)

                return returns
        except Exception:
            track = traceback.format_exc()
            print(track)
            os._exit(0)

    def getBasePath(self):
        return basePath

    def getCorePath(self):
        return corePath

    def getAppsPath(self):
        return appPath

    def quit(self):
        command = "/bin/sh " + basePath + "stop.sh"
        os.system(command)
        os._exit(0)

    def screenshot(self):
        imagePath = "/mnt/us/images"
        command = "/usr/sbin/screenshot"
        os.system(command)
        title = KcommandParam(key="title", value="Screenshot")
        message = KcommandParam(
            key="message", value="Screenshot taken")
        self.publish(Notify([title, message]), self)
        os.mkdir(imagePath)
        path = "/mnt/us"
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        file = max(paths, key=os.path.getctime)
        shutil.copy(file, imagePath)

    def main(self):
        self.scanApps()

        self.subscribe(Quit(), self.quit, self)
        self.subscribe(Screenshot(), self.screenshot, self)
        self.subscribe(FlushScreen(), self.flushScreen, self)

        print("starting webserver...")
        HTTPRESTHandler.ctx = self
        httpd = HTTPServer(('127.0.0.1', 8000), HTTPRESTHandler)

        while True:
            httpd.handle_request()


if __name__ == "__main__":
    # execute only if run as a script
    Core().main()
