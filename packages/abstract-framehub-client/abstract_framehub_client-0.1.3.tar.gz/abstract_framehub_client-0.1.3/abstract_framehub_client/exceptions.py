class ValidationException(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Validation failed")


class AlreadyExistsException(Exception):
    def __init__(self, e):
        super().__init__(e.details())


class AfhException(Exception):
    def __init__(self, e):
        super().__init__(e.details())