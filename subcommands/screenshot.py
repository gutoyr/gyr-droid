import logging

from lib.utils import get_info
from lib.utils import get_input
from lib.utils import is_secure_device
from lib.utils import take_screenshot


LOG = logging.getLogger(__name__)


def run(args):
    info_dict = get_info()
    secure = "S" if is_secure_device() else "NS"
    filename = "{}-{}-{}-{}-{}-{}.png".format(
        info_dict['ro.boot.hardware.sku'],
        info_dict['ro.carrier'],
        info_dict['ro.serialno'],
        secure,
        info_dict['ro.build.type'],
        info_dict['ro.build.id']
    )

    cont = True
    while cont:
        LOG.info("SCREENSHOT SAVED AS %s", take_screenshot(filename))
        resp = get_input("Take another screenshot? [Y/n] ")
        cont = resp != 'n'
