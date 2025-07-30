class InvalidDateRangeException(Exception):
    """Raised when the start date is after the end date."""
    def __init__(self, start_date, end_date, message=None):
        if message is None:
            message = f"Start date '{start_date}' must be earlier than end date '{end_date}'."
        super().__init__(message)
        self.start_date = start_date
        self.end_date = end_date

class NotEqualSizeException(Exception):
    """Raised when arrays are not equal length."""
    def __init__(self, message=None):
        if message is None:
            message = "Passed arrays are not equal length."
        super().__init__(message)