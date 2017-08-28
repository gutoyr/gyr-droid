class DroidException(Exception):

    DEFAULT_MESSAGE = "Failure"

    def __init__(self, message=None, **kwargs):
        if message is None:
            message = self.DEFAULT_MESSAGE % kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        super(DroidException, self).__init__(message)


class SubcommandError(DroidException):
    DEFAULT_MESSAGE = (
        "cmd: %(cmd)s\n"
        "return code: %(returncode)i\n"
        "stdout: %(stdout)s\n"
        "stderr: %(stderr)s\n")


class UnknowCommandModuleError(DroidException):
    DEFAULT_MESSAGE = "Neither fastboot nor adb commands can be executed"


class MissingFilenameError(DroidException):
    DEFAULT_MESSAGE = "Missing file name"
