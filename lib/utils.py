import logging
import subprocess
import sys

from .exception import MissingFilenameError
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
        if 'cygwin' == sys.platform:
            output = output.decode('utf-8')
            error_output = error_output.decode('utf-8')

    LOG.debug("STDOUT: %s", output)
    LOG.debug("STDERR: %s", error_output)

    if process.returncode not in success_return_codes:
        raise SubcommandError(cmd=cmd, returncode=process.returncode,
                              stdout=output, stderr=error_output)

    return output.rstrip(), error_output.rstrip()


def run_adb(args):
    cmd = "adb {}".format(args)
    return run_cmd(cmd)


def run_fastboot(args):
    cmd = "fastboot {}".format(args)
    return run_cmd(cmd)


def get_input(message):
    result = None
    if sys.version_info[0] >= 3:
        result = input(message)
    else:
        result = raw_input(message)
    return result


def is_secure_device():
    args = 'shell getprop ro.boot.secure_hardware'
    out, _ = run_adb(args)
    return '1' == out


def get_info():
    args_list = [
        "gsm.version.baseband",
        "ro.carrier",
        "ro.hw.device",
        "ro.boot.hardware.sku",
        "ro.boot.secure_hardware",
        "ro.serialno",
        "ro.build.fingerprint",
        "ro.build.description",
        "ro.build.id",
        "ro.build.tags",
        "ro.build.type",
        # "ro.product.display"
    ]

    info_dict = {}
    base_args = "shell getprop {}"
    for args in args_list:
        info_dict[args] = run_adb(base_args.format(args))[0]

    return info_dict


def take_screenshot(filename=None):
    if filename is None:
        raise MissingFilenameError()

    args_list = [
        "shell screencap -p /sdcard/{}",
        "pull /sdcard/{}",
        "shell rm /sdcard/{}",
    ]
    for args in args_list:
        run_adb(args.format(filename))

