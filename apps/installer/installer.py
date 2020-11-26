import os
import json
import urllib2
import ssl

appFolder = None


def register():
    global appFolder
    print("register Installer")
    path = os.path.dirname(os.path.realpath(__file__))
    appFolder = path.split("kapps")[1]
    return {"icon": "res/icon.png", "name": "Installer"}


def handle(path):
    if "/res" in path:
        # app resource requested
        return {"code": 200, "content": getRes(path.replace("/", "", 1))}
    if path.startswith(appFolder + "/download"):
        print("download triggered")

        appName = path.split(appFolder + "/download")[1].replace("/", "", 1)

        request = urllib2.Request(
            'https://raw.githubusercontent.com/PhilippMundhenk/kapps-list/main/list')
        response = urllib2.urlopen(
            request, context=ssl._create_unverified_context())
        listFile = response.read().decode('utf-8')
        parsed = json.loads(listFile)

        for a in parsed["apps"]:
            if a["name"] == appName:
                with open('/tmp/' + appName + '.kapp', 'wb') as f:
                    request = urllib2.Request(a["url"])
                    response = urllib2.urlopen(
                        request, context=ssl._create_unverified_context())
                    f.write(response.read())
                    f.close()

                command = "mkdir /tmp/" + a["name"]
                os.system(command)
                command = "unzip /tmp/" + appName + \
                    ".kapp -d /tmp/" + a["name"]
                os.system(command)
                command = "mv /tmp/" + a["name"] + " /mnt/us/kapps/apps"
                os.system(command)
                command = "rm /tmp/" + a["name"] + ".kapp"
                os.system(command)

        # TODO: redirect to app install screen
        return {"code": 200, "content": "None"}
    elif path.split(appFolder)[1] == "":
        # app is started

        text = ""

        # TODO: This should be fixed. Make sure cert is verified
        request = urllib2.Request(
            'https://raw.githubusercontent.com/PhilippMundhenk/kapps-list/main/list')
        response = urllib2.urlopen(
            request, context=ssl._create_unverified_context())
        listFile = response.read().decode('utf-8')
        parsed = json.loads(listFile)

        for a in parsed["apps"]:
            text = text + "<td><a href=\"" + appFolder + \
                "/download/" + a["name"] + "\"><h3>" + \
                a["name"] + "</h3></a></td>"

        with open(appFolder.replace("/", "", 1) + '/res/list.html', 'r') as file:
            return {"code": 200, "content": file.read().replace("$APPS$", text)}
    else:
        return {"code": 404, "content": "<html><h1>Not Found</h1></html>"}


def getRes(path):
    with open(path, 'r') as file:
        return file.read()
