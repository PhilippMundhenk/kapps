from BaseHTTPServer import BaseHTTPRequestHandler
from core.kcommand import KcommandParam
from core.commands import Launcher
from core.httpResponse import HTTPResponse
from core.errors import Kerror


class HTTPRESTHandler(BaseHTTPRequestHandler):
    ctx = None
    cnt = 0

    def getRes(self, path):
        with open(path.replace("/", "", 1), 'r') as file:
            return file.read()

    def error(self, techMsg, guiMsg):
        self.send_response(404)
        self.end_headers()
        self.wfile.write('<html><head><meta http-equiv = "refresh" content = "2; url = /" /></head>' +
                         '<h1 align="center">Error!</h1><br><p>' +
                         guiMsg + '</p><br/><br/>' + '<p>' + techMsg + '</p>' + '</html>')

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

            if isinstance(resp, HTTPResponse):
                self.send_response(resp.returnCode)
                if resp.headers is not None:
                    for h in resp.headers:
                        self.send_header(h[0], h[1])
                self.end_headers()
                if resp.content is not None:
                    self.wfile.write(resp.content)
            elif isinstance(resp, Kerror):
                self.error(resp.technicalMessage, resp.guiMessage)
            else:
                print("ERROR! Expected HTTPResponse...")
                # TODO: Add proper Error handling here

        elif self.path == '/':
            resp = self.ctx.publish(Launcher())[0]
            if resp is None:
                print("ERROR!")
            self.send_response(resp.returnCode)
            self.end_headers()
            self.wfile.write(resp.content)
        elif self.path.startswith("/core/res/"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.getRes(self.path))
        else:
            self.error("Command/Resource not found", "Something went wrong...")

            return
