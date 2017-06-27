import logging

from lib.utils import get_input
from lib.utils import is_secure_device
from lib.utils import run_adb as adb
from lib.utils import run_fastboot as fastboot


LOG = logging.getLogger(__name__)


def run(args):
    fastboot_args_list = [
        '-w',
        'erase userdata',
        'erase cache',
        'erase modemst1',
        'erase modemst2',
        'oem fb_mode_clear',
        'reboot',
    ]

    if is_secure_device():
        LOG.info("SECURE DEVICE")
    else:
        factory_reset = 'erase frp'
        fastboot_args_list.insert(1, factory_reset)
        LOG.info("NON SECURE DEVICE")

    LOG.info("Changing to fastboot mode...")
    adb('reboot bootloader')

    resp = get_input("Is device in fastboot mode? [Y/n] ")

    if resp != 'n':
        for fastboot_args in fastboot_args_list:
            fastboot(fastboot_args)
        LOG.info("Cleanup device done!")
