#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2022 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""""""

import time
start_time = time.time()

from omicron_gap.gap_utils import read_trig_file
import argparse
import logging
from pathlib import Path
import re
import sys
from ._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'omicron-gap'

fpat = '^(.+)-(\\d+)-(\\d+).(.+)$'
fmatch = re.compile(fpat)

logging.basicConfig()
logger = logging.getLogger(__process_name__)
logger.setLevel(logging.DEBUG)


def count_trigs(ext, flist):
    """
    Count the number of triggers in the list of files
    :param ext:
    :param flist:
    :return:
    """
    count = 0
    duration = 0

    for path in flist:
        try:
            table, name, strt, dur = read_trig_file(path)
        except (ValueError, FileNotFoundError) as ex:
            logger.error(f'Problem reading {path.absolute()}: {ex}')
            continue

        duration += dur
        count1 = 0 if table is None else len(table)
        logger.debug(f'{name}, {strt}, {dur}, {count1}')
        count += count1
    return count, duration


def main():

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')

    parser.add_argument('indirs', type=Path, nargs=2, help='2 directories to compare')
    parser.add_argument('--ext', help='trigger type (root, h5, xml')
    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    # debugging?
    logger.debug('{} called with arguments:'.format(__process_name__))
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    a = Path(args.indirs[0])
    b = Path(args.indirs[1])

    ext = args.ext
    glob_pat = f'*.{ext}*'
    afiles = list(a.glob(glob_pat))
    logger.debug(f'Directory: {a.absolute()}')
    afiles.sort()
    acount, adur = count_trigs(ext, afiles)

    bfiles = list(b.glob(glob_pat))
    logger.debug(f'Directory: {b.absolute()}')
    bfiles.sort()
    bcount, bdur = count_trigs(ext, bfiles)

    if acount == bcount and adur == bdur:
        success = 'Success'
        ret = 0
    else:
        success = 'Failure'
        ret = 1

    logger.info(f'{success}: Counts: {acount} vs. {bcount}, Duration: {adur} vs {bdur} '
                f'Files: {len(afiles)} vs {len(bfiles)}')

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
    return ret


if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
