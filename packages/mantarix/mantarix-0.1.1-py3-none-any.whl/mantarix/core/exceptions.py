class MantarixException(Exception):
    pass


class MantarixUnsupportedPlatformException(MantarixException):
    """
    Thrown by operations that are not supported on the current platform.
    """

    def __init__(self, message: str):
        super().__init__(message)


class MantarixUnimplementedPlatformEception(MantarixUnsupportedPlatformException):
    """
    Thrown by operations that have not been implemented yet.
    """

    pass
