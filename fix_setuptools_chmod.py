# Quick and dirty trick to fix executable permissions spuriously
# set by the setuptools.

__all__ = []

# version
__id__ = "$Id: fix_setuptools_chmod.py 2819 2009-03-08 01:31:22Z juhas $"

import os
import stat
import setuptools
from pkg_resources import parse_version


# adjusted from setuptools-0.6c8

try:
    from os import chmod as _chmod
except ImportError:
    # Jython compatibility
    def _chmod(*args): pass


def chmod(path, mode):
    from distutils import log
    log.debug("changing mode of {0!s} to {1:o}", path, mode)
    try:
        _chmod(path, mode)
    except os.error as e:
        log.debug("chmod failed: {0!s}", e)


def fixed_unpack_and_compile(self, egg_path, destination):
    from setuptools.archive_util import unpack_archive
    to_compile = []; to_chmod = []

    def pf(src, dst):

        if dst.endswith('.py') and not src.startswith('EGG-INFO/'):
            to_compile.append(dst)
            to_chmod.append(dst)
        elif dst.endswith('.dll') or dst.endswith('.so'):
            to_chmod.append(dst)
        self.unpack_progress(src, dst)
        return not self.dry_run and dst or None

    unpack_archive(egg_path, destination, pf)
    self.byte_compile(to_compile)
    if not self.dry_run:
        for f in to_chmod:
#           mode = ((os.stat(f)[stat.ST_MODE]) | 0o555) & 0o7755
            mode = ((os.stat(f)[stat.ST_MODE]) | 0o444) & 0o7755
            chmod(f, mode)

    to_compile = []; to_chmod = []
    return


# Hack the easy_install class for versions compatible with
# fixed_unpack_and_compile
if parse_version(setuptools.__version__) <= parse_version('0.6c9'):
    from setuptools.command.easy_install import easy_install
    easy_install.unpack_and_compile = fixed_unpack_and_compile

# End of file
