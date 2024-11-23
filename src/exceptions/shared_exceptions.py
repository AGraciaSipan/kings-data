class InvalidUUIDException(ValueError):
    def __init__(self, value: str):
        self.message = f"The provided ID '{value}' is not a valid UUID."
        super().__init__(self.message)
