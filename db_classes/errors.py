class PresenceError(Exception):
    pass
class RecordError(Exception):
    def __init__(self) -> None:
        self.message = "parameters were underspecified for the target function"
        super().__init__(self.message)