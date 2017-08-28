import logging

from lib.device import change_to_fastboot_mode
from lib.device import cleanup
from lib.device import is_fastboot_mode
from lib.device import reboot
from lib.utils import get_input


LOG = logging.getLogger(__name__)


def run(args):
    if not is_fastboot_mode():
        resp = get_input("Change device to fastboot mode? [y/n] ")
        if resp == 'y':
            change_to_fastboot_mode()
        else:
            return

    cleanup()
    LOG.info("Cleanup device done!")

    resp = get_input("Reboot device? [y/n] ")
    if resp != 'n':
        reboot()
