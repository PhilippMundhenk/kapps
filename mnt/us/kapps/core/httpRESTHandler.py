from BaseHTTPServer import BaseHTTPRequestHandler
from core.kcommand import KcommandParam
from core.commands import Launcher


class HTTPRESTHandler(BaseHTTPRequestHandler):
    ctx = None
    cnt = 0

    def getRes(self, path):
        with open(path.replace("/", "", 1), 'r') as file:
            return file.read()

    def do_GET(self):
        HTTPRESTHandler.cnt = HTTPRESTHandler.cnt + 1
        if HTTPRESTHandler.cnt > 20:
            self.ctx.flushScreen()
            HTTPRESTHandler.cnt = 0

        if self.path.startswith('/apps'):
            print("path = " + self.path)
            kcommandHash = self.path.split("/")[2]
            paramString = self.path.replace(
                "/apps", "").replace("/" + kcommandHash + "/", "")
            params = []
            print("params len=" + str(len(params)))
            if len(paramString) > 0:
                paramList = paramString.split("/")
                for p in paramList:
                    if p != "":
                        params.append(KcommandParam(string=p))

            resp = None
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
            resp = self.ctx.publish(Launcher())[0]
            if resp is None:
                print("ERROR!")
            self.send_response(resp["code"])
            self.end_headers()
            self.wfile.write(resp["content"])
        elif self.path.startswith("/core/res/"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.getRes(self.path))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            return
