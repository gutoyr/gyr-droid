import logging

from lib.utils import is_fastboot_mode
from lib.utils import get_input
from lib.utils import is_secure_device
from lib.utils import run_fastboot as fastboot


LOG = logging.getLogger(__name__)


def run(args):
    is_fastboot_mode()

    fastboot_args_list = [
        '-w',
        'erase userdata',
        'erase cache',
        'erase modemst1',
        'erase modemst2',
        'oem fb_mode_clear',
    ]

    if is_secure_device():
        LOG.info("SECURE DEVICE")
    else:
        factory_reset = 'erase frp'
        fastboot_args_list.insert(1, factory_reset)
        LOG.info("NON SECURE DEVICE")

    for fastboot_args in fastboot_args_list:
        fastboot(fastboot_args)
    LOG.info("Cleanup device done!")

    resp = get_input("Reboot device? [Y/n] ")
    if resp != 'n':
        fastboot('reboot')
