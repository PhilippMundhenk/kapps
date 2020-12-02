from core.kcommand import Kcommand


class Quit(Kcommand):
    def __init__(self):
        super(Quit, self).__init__(
            "Quit", "kapps-quit-command-hash")
