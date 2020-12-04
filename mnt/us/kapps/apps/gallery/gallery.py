from core.kapp import Kapp
from core.httpResponse import HTTPResponse
from core.Kcommand import Kcommand
import uuid
import os
import time


class GetImage(Kcommand):
    getImageHash = str(uuid.uuid4())

    def __init__(self):
        super(GetImage, self).__init__(
            "GetImage", self.getImageHash)


class ViewImage(Kcommand):
    viewImageHash = str(uuid.uuid4())

    def __init__(self):
        super(ViewImage, self).__init__(
            "ViewImage", self.viewImageHash)


class GalleryApp(Kapp):
    name = "Gallery"

    def getImageCallback(self, kcommand):
        with open(kcommand.getParameter("path"), 'r') as file:
            return HTTPResponse(content=file.read())

    def viewImageCallback(self, kcommand):
        cmd = GetImage()
        cmd.params = dict(kcommand.params)
        return HTTPResponse(content=self.getRes("image.html").replace("$IMAGE$", "<img style=\"width:100%;\" src=" + cmd.toURL() + " />"))

    def homeCallback(self, kcommand):
        path = "/mnt/us/images/"
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]

        text = ""
        for p in paths:
            text = text + "<tr><td>"
            imageURL = ViewImage().setParameter("path", p).toURL()
            text = text + "<a href=\"" + \
                imageURL + "\">" + p.replace(path, "") + "</a>"
            text = text + "</td></tr>"
        return HTTPResponse(content=self.getRes("imageList.html").replace("$IMAGES$", text))

    def iconCallback(self, kcommand):
        return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    print("register " + GalleryApp.name)
    app = GalleryApp(appID, appPath, ctx)
    app.subscribe(GetImage(), app.getImageCallback)
    app.subscribe(ViewImage(), app.viewImageCallback)

    return app
