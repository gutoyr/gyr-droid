import logging
import os
import time

from lib.device import get_info
from lib.device import is_fastboot_mode
from lib.device import is_secure
from lib.device import reboot
from lib.device import take_screenshot
from lib.utils import get_input


LOG = logging.getLogger(__name__)
FILENAME_TEMPLATE = '{filename}_{timestamp}{extension}'
FILE_EXTENSION = '.png'


def run(args):
    if is_fastboot_mode():
        resp = get_input("Device is in fastboot mode. Reboot? [y/n] ")
        if resp == 'y':
            reboot(wait=True)
        else:
            return

    if args.get('filename') is None:
        secure = 'S' if is_secure() else 'NS'
        base_filename = (
            '{sku}_{carrier}_{serialno}_{secure}_{build_id}').format(
                sku=get_info('ro.boot.hardware.sku'),
                carrier=get_info('ro.carrier'),
                serialno=get_info('ro.serialno'),
                secure=secure,
                build_id=get_info('ro.build.id'),)
        file_extension = FILE_EXTENSION
    else:
        base_filename, file_extension = os.path.splitext(
            args.get('filename')[0])

    timestamp = 0

    while get_input("Take screenshot? [Y/n] ") != 'n':
        if args.get('serial'):
            timestamp = time.time()
        else:
            timestamp += 1
        filename = FILENAME_TEMPLATE.format(filename=base_filename,
                                            timestamp=timestamp,
                                            extension=file_extension)
        take_screenshot(filename)
        LOG.info("SCREENSHOT SAVED AS %s", filename)
