from .exception import MissingFilenameError
from .utils import run_cmd


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


def get_default_start_activity(package):
    cmd = "cmd package resolve-activity --brief {} | tail -n 1".format(package)
    return run_shell(cmd)[0].split('/')[1]


def get_current_screen_package_activity():
    cmd = "dumpsys window windows | grep 'mCurrentFocus'"
    out, _ = run_shell(cmd)
    package_activity = out.split()[-1].split('/')
    package = package_activity[0]
    activity = package_activity[1].rstrip('}')
    return package, activity


def start_application(package, activity=None):
    if activity is None:
        activity = get_default_start_activity(package)

    cmd = "am start {}/{}".format(package, activity)
    return run_shell(cmd)
