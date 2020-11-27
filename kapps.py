from BaseHTTPServer import HTTPServer
from core.httpRESTHandler import HTTPRESTHandler
import importlib
import pkgutil
import uuid

import apps


class Core():
    apps = {}

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
        print("scanning apps...")
        AllApps = self.import_submodules(apps)

        for name in AllApps:
            print("found " + name)

            alreadyRegistered = False
            for a in self.apps:
                if name.startswith(self.apps[a].getAppPythonPath()):
                    print("skipping " + name + " (already registered)")
                    alreadyRegistered = True

            if not alreadyRegistered:
                try:
                    register = getattr(AllApps[name], "register")
                    appID = uuid.uuid1()
                    app = register(appID, name.rsplit(".", 1)[0], self)
                    self.apps[appID] = app
                except AttributeError:
                    pass

    def removeApp(self, app):
        for a in self.apps:
            if self.apps[a] == app:
                self.apps.pop(a)
                break

    def getApps(self):
        return self.apps

    def getAppByIDString(self, id):
        return self.apps[uuid.UUID(id)]

    def getAppByID(self, id):
        return self.apps[id]

    def getAppByPythonPath(self, path):
        for a in self.apps:
            if self.apps[a].getAppPythonPath() == path:
                return self.apps[a]

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
