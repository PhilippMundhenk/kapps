# kapps
kapps is a rudimentary app framework for Kindles with E Ink displays, such as the Kindle Touch, among many others. These devices run Linux and, with a jailbreak, can be made to run any software. This framework is based on a combination of Python and web technologies, allowing the implementation of applications, or apps, with or without graphical user interface (GUI). By providing a framework for communication between apps and the GUI, as well as defining a basic package format, apps can be easily loaded, and communicate with each other, as well as the GUI.

Not that this project is still in a very early stage, I might gradually extend it based on my needs and possible requests. I welcome any contributions.

## Features

- Setup for GUI to backend connection, no need to handle webserver, URLs, etc.
- Application definitions, including (un-)installing from web
- Commands for communication between applications and GUI
- Notification system

## Basic Application

The Quit application is a very basic application without GUI. It consists of only a few files:

```
Quit/
├─ res/
│  ├─ icon.png
├─ __init__.py
├─ quit.py
```

The implementation is as simple as this:

```py
from core.kapp import Kapp
from core.commands import Quit, Launcher
from core.httpResponse import HTTPResponse


class QuitApp(Kapp):
    name = "Quit"

    def homeCallback(self, kcommand):
        self.publish(Quit())
        return self.publish(Launcher())[0]

    def iconCallback(self, kcommand):
    	return HTTPResponse(content=self.getRes("icon.png"))


def register(appID, appPath, ctx):
    return QuitApp(appID, appPath, ctx)
```

## Requirements

- Kindle Touch: Likely also running on other Kindles, but not tested.
- Jailbreak for Kindle Touch, see [here](https://www.mobileread.com/forums/showthread.php?t=275877)
- (optional) USB Networking, see [here](https://www.mobileread.com/forums/showthread.php?t=186645)
- WebLaunch, see [here](https://github.com/PaulFreund/WebLaunch)
- Python, see [here](https://www.mobileread.com/forums/showthread.php?t=225030)

Technically, WebLaunch is not required, as it uses the internal browser, but it is a nice wrapper, that I have not yet fully integrated. It is also an extension for KUAL, the Kindle Unified Application Launcher, which we will not be using.

## Screenshots

### Launcher

![Launcher](screenshots/launcher.png)

### Installer

![Installer](screenshots/installer.png)

### Uninstaller

![Uninstaller](screenshots/uninstaller.png)

### Notifications

![Notifications](screenshots/notifications.png)

### Gallery

![Gallery](screenshots/gallery.png)
![Gallery](screenshots/gallery2.png)

## Improvements

I only built what I needed so far, the feature set might change in future, upon needs and requests. Here are some things on the very top of the list:

- A proper, extensible logging system
- Tests
- An improved documentation, including API and examples
- Minimizing dependencies: Use browser directly without WebLaunch
- Easier install procedure
- Wrap more lipc commands (see [MobileRead Wiki](https://wiki.mobileread.com/wiki/Lipc))
- Self-update of core and minimize applications in core
- Dependency management for applications
- Better update management for applications (e.g., by including and checking version numbers)
- Support for more repositories to install
- Storage application for non-volatile storage (e.g., key-value store)
- Settings file and application
- WebSockets or similar to make GUI more responsive

