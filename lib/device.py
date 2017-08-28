import logging
import time

from . import adb
from . import fastboot

from .exception import UnknowCommandModuleError


LOG = logging.getLogger(__name__)


def _get_cmd_module():
    out, _ = adb.run('devices')
    out_list = out.split()
    if len(out_list) >= 5:
        return adb

    out, _ = fastboot.run('devices')
    out_list = out.split()
    if len(out.split()) >= 2:
        return fastboot

    raise UnknowCommandModuleError


def select_cmd_module(fun):
    def wrapper(*args, **kwargs):
        cmd_module = _get_cmd_module()
        try:
            new_fun = getattr(cmd_module, fun.__name__)
            return new_fun(*args, **kwargs)
        except AttributeError:
            LOG.error("%s can not be executed by %s", fun.__name__, cmd_module)
    return wrapper


@select_cmd_module
def run(param):
    pass


@select_cmd_module
def is_secure():
    pass


@select_cmd_module
def get_info(param):
    pass


@select_cmd_module
def take_screenshot(param):
    pass


@select_cmd_module
def cleanup():
    pass


def is_fastboot_mode():
    return _get_cmd_module() == fastboot


def change_to_fastboot_mode():
    if _get_cmd_module() == adb:
        adb.run('reboot bootloader')
        time.sleep(3)


def reboot(wait=False):
    cmd_module = _get_cmd_module()
    cmd_module.run('reboot')
    if wait:
        adb.run('wait-for-device')
