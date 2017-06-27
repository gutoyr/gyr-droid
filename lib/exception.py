class BaseException(Exception):

    DEFAULT_MESSAGE = "Failure"

    def __init__(self, message=None, **kwargs):
        if message is None:
            message = self.DEFAULT_MESSAGE % kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        super(BaseException, self).__init__(message)


class SubcommandError(BaseException):
    DEFAULT_MESSAGE = (
        "cmd: %(cmd)s\n"
        "return code: %(returncode)i\n"
        "stdout: %(stdout)s\n"
        "stderr: %(stderr)s\n")
