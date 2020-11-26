from BaseHTTPServer import HTTPServer
from core.httpRESTHandler import HTTPRESTHandler
import importlib
import pkgutil

import apps


class Core():
    appDetails = {}
    appHandlers = {}

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

    def getAppDetails(self):
        return self.appDetails

    def getAppHandlers(self):
        return self.appHandlers

    def main(self):
        AllApps = self.import_submodules(apps)

        for name in AllApps:
            # print(name)
            # print(AllApps[name])
            try:
                register = getattr(AllApps[name], "register")
                app = register()
                self.appDetails[name.rsplit('.', 1)[0]] = app
                self.appHandlers[name.rsplit('.', 1)[0]] = getattr(AllApps[name], "handle")
            except AttributeError:
                pass

        print("starting webserver...")
        HTTPRESTHandler.ctx = self
        httpd = HTTPServer(('127.0.0.1', 8000), HTTPRESTHandler)

        while True:
            httpd.handle_request()


if __name__ == "__main__":
    # execute only if run as a script
    Core().main()
