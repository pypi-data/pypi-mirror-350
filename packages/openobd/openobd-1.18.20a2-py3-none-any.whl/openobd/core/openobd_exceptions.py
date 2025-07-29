
class OpenOBDException(Exception):
    """
    Base class for all exceptions that can be raised when using the openobd library.
    """

    def __init__(self, details="", status=-1, status_description=""):
        self.details = details
        self.status = status
        self.status_description = status_description

    def __str__(self):
        exception_info = self.__class__.__name__

        if self.details:
            exception_info += f": {self.details}"
        if self.status != -1:
            exception_info += f" (gRPC status: {self.status}"
            if self.status_description:
                exception_info += f", {self.status_description}"
            exception_info += ")"

        return exception_info
