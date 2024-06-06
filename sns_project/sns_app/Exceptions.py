class CustomException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message, self.error_code)


class ExtraFieldsError(Exception):
    def __init__(self, extra_fields):
        self.extra_fields = extra_fields
        self.message = f"Extra fields found: {', '.join(extra_fields)}"
        self.error_code = 1212
        super().__init__(self.message, self.error_code)
