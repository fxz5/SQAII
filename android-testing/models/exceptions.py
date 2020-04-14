class CallFailed(Exception):
    def __init__(self, value):
        self.value = "could not complete call because of " + value

    def __str__(self):
        return repr(self.value)
