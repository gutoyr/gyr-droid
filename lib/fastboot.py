from .utils import run_cmd


def clear_output(output):
    out = list()
    for line in output.split('\n'):
        if (not line.startswith('(bootloader) slot-') and
                not line.startswith('finished.')):
            out.append(line.rstrip())
    return out


def run(args, clean=True):
    cmd = "fastboot {}".format(args)
    out, err = run_cmd(cmd)
    if clean:
        err = clear_output(err)
    return out, err


def is_secure():
    args = 'getvar secure'
    _, out = run(args)
    return 'yes' in out[0]


def get_info(param):
    args = 'getvar {}'.format(param)
    output = run(args)[1]
    if len(output) > 1 and 'Done' in output[-1]:
        del output[-1]
    info = ''.join(i.split(': ')[1] for i in output)
    return info


def cleanup():
    args_list = [
        '-w',
        'erase userdata',
        'erase cache',
        'erase modemst1',
        'erase modemst2',
        'oem fb_mode_clear',
        'erase frp',
    ]

    for args in args_list:
        run(args)
# fastboot oem hw dualsim true
# fastboot oem config sku XT1710-07
