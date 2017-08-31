import logging
import time

from .exception import MissingFilenameError
from .utils import run_cmd

LOG = logging.getLogger(__name__)
WAIT_TIME = 2


def _get_display_size():
    args = "dumpsys window displays | grep init="
    out, _ = run_shell(args)
    return out.split()[0].split('=')[1].split('x')


def run(args):
    cmd = "adb {}".format(args)
    return run_cmd(cmd)


def run_shell(args):
    cmd = "shell {}".format(args)
    return run(cmd)


def is_secure():
    args = 'shell getprop ro.boot.secure_hardware'
    out, _ = run(args)
    return out == '1'


def get_info(param):
    args = "shell getprop {}".format(param)
    return run(args)[0]


def take_screenshot(filename):
    if filename is None:
        raise MissingFilenameError()

    args_list = [
        "shell screencap -p /sdcard/{}",
        "pull /sdcard/{}",
        "shell rm /sdcard/{}",
    ]
    for args in args_list:
        run(args.format(filename))


def send_keycode(keycode):
    args = "input keyevent {}".format(keycode)
    run_shell(args)


def send_text(text):
    args = "input text \"{}\"".format(text)
    run_shell(args)


def send_tap(x, y):
    if x < 1 and y < 1:
        size = _get_display_size()
        x = int(x * int(size[0]))
        y = int(y * int(size[1]))
    args = "input tap {} {}".format(x, y)
    run_shell(args)


def get_default_start_activity(package):
    cmd = "cmd package resolve-activity --brief {} | tail -n 1".format(package)
    return run_shell(cmd)[0].split('/')[1]


def _get_current_apk_activity():
    cmd = "dumpsys window windows | grep 'mCurrentFocus'"
    out, _ = run_shell(cmd)
    package_activity = out.split()[-1].split('/')
    package = package_activity[0]
    activity = package_activity[1].rstrip('}')
    return package, activity


def get_current_apk():
    return _get_current_apk_activity()[0]


def get_current_activity():
    return _get_current_apk_activity()[1]


def wait_for_activity(activity):
    LOG.debug('Expected activity: ' + activity)
    while True:
        try:
            current_activity = get_current_activity()
            LOG.debug('Current activity: ' + current_activity)
            time.sleep(WAIT_TIME)
            if current_activity == activity:
                break
        except IndexError:
            pass


def start_application(package, activity=None):
    if activity is None:
        activity = get_default_start_activity(package)

    cmd = "am start {}/{}".format(package, activity)
    return run_shell(cmd)
