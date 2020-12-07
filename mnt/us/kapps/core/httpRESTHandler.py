from BaseHTTPServer import BaseHTTPRequestHandler
from core.commands import Launcher, FlushScreen
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
            self.ctx.publish(FlushScreen())
            HTTPRESTHandler.cnt = 0

        if self.path.startswith('/apps'):
            print("path = " + self.path)
            kcommandHash = self.path.split("/")[2]
            print("kcommandHash = " + kcommandHash)
            paramString = self.path.replace(
                "/apps", "").replace("/" + kcommandHash, "")
            print("paramString = " + paramString)
            kcommand = self.ctx.getKcommand(kcommandHash)
            print("kcommand = " + str(kcommand))
            kcommand.paramsFromString(paramString)
            resps = self.ctx.publish(kcommand)
            print("resps = " + str(resps))
            resp = resps[0]

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
