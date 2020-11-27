from BaseHTTPServer import BaseHTTPRequestHandler
import re


class HTTPRESTHandler(BaseHTTPRequestHandler):
    ctx = None

    def getLauncher(self):
        # TODO: Insert reading of apps here!
        text = "<tr>"
        cnt = 0
        for uuid, app in sorted(self.ctx.getApps().items(), key=lambda x: x[1].name):
#        for uuid, app in self.ctx.getApps().items():
            text = text + "<td>" + "<p align=\"center\"><a href=\"" + app.getAppURL() + "\"><img border=\"0\" src=\"" + \
                app.getAppURL() + "/" + app.icon + "\"/><br>" + app.name + "</a></p>" + "</td>"

            cnt = cnt + 1
            if cnt % 3 == 0:
                text = text + "</tr><tr>"
        text = text + "</tr>"

        with open('core/res/launcher.html', 'r') as file:
            return file.read().replace("$APPS$", text)

    def do_GET(self):
        if self.path.startswith('/apps'):
            appID = self.path.split("/")[2]
            resp = self.ctx.getAppByIDString(appID).handleGet(self.path)
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
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            return
