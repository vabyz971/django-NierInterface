# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T10:18:13-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-09-03T16:41:40-04:00
# @License: GPLv3

VERSION = (0, 1, 2, "f")  # following PEP 386
DEV_N = None


def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s" % (version, VERSION[3])
        if DEV_N:
            version = "%s.dev%s" % (version, DEV_N)
    return version


__author__ = "vabyz971"
__license__ = "GPL-V3"
__version__ = get_version()
default_app_config = 'nierInterface.apps.AppConfig'
