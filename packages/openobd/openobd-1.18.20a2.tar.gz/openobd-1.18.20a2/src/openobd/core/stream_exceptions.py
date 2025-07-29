from .openobd import OpenOBDException


class OpenOBDStreamException(OpenOBDException):
    """
    Exception that can occur when handling gRPC streams.
    """
    pass


class OpenOBDStreamStoppedException(OpenOBDStreamException):
    pass


class OpenOBDStreamTimeoutException(OpenOBDStreamException):
    pass
