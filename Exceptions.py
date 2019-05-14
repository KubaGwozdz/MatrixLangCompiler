class ReturnValueException(Exception):
    def __init__(self, value):
        self.value = value


class BreakException(Exception):
    #print("BREAK EXCEPTION")
    pass


class ContinueException(Exception):
    #print("CONTINUE EXCEPTION")
    pass