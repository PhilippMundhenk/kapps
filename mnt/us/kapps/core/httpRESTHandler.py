from BaseHTTPServer import BaseHTTPRequestHandler
from core.kcommand import KcommandParam


class HTTPRESTHandler(BaseHTTPRequestHandler):
    ctx = None
    cnt = 0

    def getRes(self, path):
        with open(path.replace("/", "", 1), 'r') as file:
            return file.read()

    def getLauncher(self):
        # TODO: Insert reading of apps here!
        text = "<tr>"
        cnt = 0
        for uuid, app in self.ctx.getSortedApps():
            text = text + "<td>" + "<p align=\"center\"><a href=\"" + app.getHomeCommand().toURL() + "\"><img border=\"0\" src=\"" + app.getIconCommand().toURL() + "\"/><br/>" + \
                app.name + "</a></p>" + "</td>"

            cnt = cnt + 1
            if cnt % 3 == 0:
                text = text + "</tr><tr>"
        text = text + "</tr>"

        with open('core/res/launcher.html', 'r') as file:
            return file.read().replace("$APPS$", text)

    def do_GET(self):
        HTTPRESTHandler.cnt = HTTPRESTHandler.cnt + 1
        if HTTPRESTHandler.cnt > 20:
            self.ctx.flushScreen()
            HTTPRESTHandler.cnt = 0

        if self.path.startswith('/apps'):
            print("self.path=" + self.path)
            kcommandHash = self.path.split("/")[2]
            print("kcommandHash=" + kcommandHash)
            paramString = self.path.replace(
                "/apps", "").replace("/" + kcommandHash + "/", "")
            print("paramString=" + paramString)
            params = []
            if len(paramString) > 0:
                paramList = paramString.split("/")
                for p in paramList:
                    if p != "":
                        params.append(KcommandParam(string=p))

                print("calling " + kcommandHash +
                      " with paramString: \"" + paramString + "\"")
                print("resulting in paramList length: " + str(len(paramList)))

            if len(params) == 0:
                resp = self.ctx.publishByKcommandHash(kcommandHash)[0]
            else:
                resp = self.ctx.publishByKcommandHash(
                    kcommandHash, data=params)[0]
            self.send_response(resp["code"])
            if "headers" in resp:
                for h in resp["headers"]:
                    self.send_header(h[0], h[1])
            self.end_headers()
            if "content" in resp:
                self.wfile.write(resp["content"])
        elif self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.getLauncher())
        elif self.path.startswith("/core/res/"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.getRes(self.path))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            return
