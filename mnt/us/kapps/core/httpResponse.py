class HTTPResponse(object):
    def __init__(self, returnCode=None, content=None, headers=None):
        if returnCode is None and content is not None:
            self.returnCode = 200
        else:
            self.returnCode = returnCode
        self.headers = headers
        self.content = content
