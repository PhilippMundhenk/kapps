from BaseHTTPServer import HTTPServer
from core.httpRESTHandler import HTTPRESTHandler
import importlib
import pkgutil
import uuid
from subprocess import call

import apps


class Core():
    systemApps = ["apps.installer", "apps.uninstaller", "apps.settings"]
    apps = {}
    subscriptions = {}

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

            alreadyRegistered = False
            for a in self.apps:
                if name.startswith(self.apps[a].getAppPythonPath()):
                    alreadyRegistered = True

            if not alreadyRegistered:
                try:
                    register = getattr(AllApps[name], "register")
                    appID = uuid.uuid1()
                    app = register(appID, name.rsplit(".", 1)[0], self)
                    self.apps[appID] = app
                except AttributeError:
                    pass

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

    def getAppByIDString(self, id):
        return self.apps[uuid.UUID(id)]

    def getAppByID(self, id):
        return self.apps[id]

    def getAppByPythonPath(self, path):
        for a in self.apps:
            if self.apps[a].getAppPythonPath() == path:
                return self.apps[a]

    def flushScreen(self):
        call(["/mnt/us/kapps/core/util/flushScreen.sh"])

    def subscribe(self, kcommand, callback, subscriber):
        if kcommand in self.subscriptions:
            self.subscriptions[kcommand.hash()].append(callback)
        else:
            self.subscriptions[kcommand.hash()] = [callback]

        print("registered " + kcommand.hash())

    def publish(self, kcommand):
        if kcommand.hash() not in self.subscriptions:
            print("no subscriber registered for " + kcommand.hash())
        else:
            for callback in self.subscriptions[kcommand.hash()]:
                callback()

    def main(self):
        self.scanApps()

        print("starting webserver...")
        HTTPRESTHandler.ctx = self
        httpd = HTTPServer(('127.0.0.1', 8000), HTTPRESTHandler)

        while True:
            httpd.handle_request()


if __name__ == "__main__":
    # execute only if run as a script
    Core().main()
