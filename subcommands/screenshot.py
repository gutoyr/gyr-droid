import logging
import os
import time

from lib.utils import get_info
from lib.utils import get_input
from lib.utils import is_secure_device
from lib.utils import take_screenshot


LOG = logging.getLogger(__name__)
FILENAME_TEMPLATE = '{filename}_{timestamp}{extension}'
FILE_EXTENSION = '.png'


def run(args):
    if args.get('filename') is None:
        info_dict = get_info()
        secure = 'S' if is_secure_device() else 'NS'
        base_filename = (
            '{sku}_{carrier}_{serialno}_{secure}_{build_type}'
            '_{build_id}').format(sku=info_dict['ro.boot.hardware.sku'],
                                  carrier=info_dict['ro.carrier'],
                                  serialno=info_dict['ro.serialno'],
                                  secure=secure,
                                  build_type=info_dict['ro.build.type'],
                                  build_id=info_dict['ro.build.id'],)
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
