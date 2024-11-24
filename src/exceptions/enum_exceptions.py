class InvalidEnumValueError(Exception):
    def __init__(self, enum_class, invalid_value):
        values = {k.value for k in enum_class}
        super().__init__(f"Invalid value: '{invalid_value}' for {enum_class.__name__}. Must be one of {values}.")
