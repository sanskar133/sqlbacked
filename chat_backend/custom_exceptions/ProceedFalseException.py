class ProceedFalseException(Exception):
    def __init__(self, message, output, step_data):
        super().__init__(message)
        self.output = output
        self.step_data = step_data
