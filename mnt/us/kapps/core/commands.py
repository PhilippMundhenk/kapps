from core.kcommand import Kcommand


class Quit(Kcommand):
    def __init__(self):
        super(Quit, self).__init__(
            "Quit", "kapps-quit-command-hash")


class Launcher(Kcommand):
    def __init__(self):
        super(Launcher, self).__init__(
            "Launcher", "kapps-launcher-command-hash")


class Notify(Kcommand):
    def __init__(self, params=None):
        super(Notify, self).__init__(
            "Notify", "kapps-notification-command-hash", params=params)
