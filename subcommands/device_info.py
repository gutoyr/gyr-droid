import logging

from lib.device import get_info
from lib.device import is_fastboot_mode
from lib.device import is_secure

LOG = logging.getLogger(__name__)


def run(args):
    key_list = [
        'baseband',
        'carrier',
        'device',
        'sku',
        'serialno',
        'build',
    ]
    if is_fastboot_mode():
        value_list = [
            "version-baseband",
            "ro.carrier",
            "product",
            "sku",
            "serialno",
            "ro.build.fingerprint",
        ]
    else:
        value_list = [
            "gsm.version.baseband",
            "ro.carrier",
            "ro.hw.device",
            "ro.boot.hardware.sku",
            "ro.serialno",
            "ro.build.fingerprint",
        ]

    info_dict = dict(zip(key_list, value_list))
    for key, value in info_dict.items():
        LOG.info("%s => %s", key, get_info(value))
    LOG.info("secure => %s", is_secure())
