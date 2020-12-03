class Kerror(Exception):
    def __init__(self, technicalMessage, guiMessage=None):
        self.technicalMessage = technicalMessage
        self.guiMessage = guiMessage
