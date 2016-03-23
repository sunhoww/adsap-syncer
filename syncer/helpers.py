import time

VALIDITY = 1800

def get_epoch(s=None):
    if s is None:
        return int(time.time())
    try:
        if len(s) < 14:
            raise ValueError
        return int(time.mktime(time.strptime(s[:14], "%Y%m%d%H%M%S")))
    except ValueError:
        return -1

def get_stime(s=None):
    if s < 0:
        return time.asctime()
    return time.asctime(time.gmtime(s))

# http://garage.pimentech.net/libcommonPython_src_python_libcommon_javastringhashcode/
def java_string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

def stamp():
    return ''
