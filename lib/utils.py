import logging
import subprocess
import sys

from .exception import SubcommandError


LOG = logging.getLogger(__name__)


def run_cmd(cmd, **kwargs):
    LOG.debug("STDIN: %s", cmd)
    shell = kwargs.pop('shell', True)
    success_return_codes = kwargs.pop('success_return_codes', [0])

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=shell, **kwargs)
    output, error_output = process.communicate()

    if sys.version_info[0] >= 3:
        if sys.platform == 'cygwin':
            output = output.decode('utf-8')
            error_output = error_output.decode('utf-8')

    LOG.debug("returncode: %s", process.returncode)
    LOG.debug("STDOUT: %s", output)
    LOG.debug("STDERR: %s", error_output)

    if process.returncode not in success_return_codes:
        raise SubcommandError(cmd=cmd, returncode=process.returncode,
                              stdout=output, stderr=error_output)

    return output.rstrip(), error_output.rstrip()


def get_input(message):
    result = None
    if sys.version_info[0] >= 3:
        result = input(message)
    else:
        result = raw_input(message) # noqa  # pylint: disable=undefined-variable
    return result
