class Error:
    def __init__(self, error, displayMessageToUser, message, origin):
        self.error = error,
        self.displayMessageToUser = displayMessageToUser,
        self.message = message,
        self.origin = origin
