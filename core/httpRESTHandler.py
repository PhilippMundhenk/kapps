from BaseHTTPServer import BaseHTTPRequestHandler
import re


class HTTPRESTHandler(BaseHTTPRequestHandler):
    ctx = None

    def getLauncher(self):
        # TODO: Insert reading of apps here!
        text = "<tr>"
        for a in self.ctx.getAppDetails():
            text = text + "<td>" + "<p align=\"center\"><a href=\"" + a.replace(".", "/") + "\"><img border=\"0\" src=\"" + a.replace(".", "/") + "/" + self.ctx.getAppDetails(
            )[a]["icon"] + "\"/><br>" + self.ctx.getAppDetails()[a]["name"] + "</a></p>" + "</td>"
        text = text + "</tr>"

        with open('core/res/launcher.html', 'r') as file:
            return file.read().replace("$APPS$", text)

    def handleApp(self, path):
        appID = path.split("/")[1] + "." + path.split("/")[2]
        print("handling app: " + appID)
        return self.ctx.getAppHandlers()[appID](path)

    def do_GET(self):
        if re.search('/apps', self.path) is not None:
            resp = self.handleApp(self.path)
            self.send_response(resp["code"])
            self.end_headers()
            self.wfile.write(resp["content"])
        elif re.search('/', self.path) is not None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(self.getLauncher())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            return
