#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2023 Joseph Areeda <joseph.areeda@ligo.org>
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

"""
Tired of tconverting segments.txt files so this is a simple script to
print omicron segments.txt files
"""
import os
import time
from datetime import timedelta

from gwpy.time import tconvert, from_gps

from omicron_gap.gap_utils import get_default_config, get_default_ifo

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
from ._version import __version__


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name


def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    ifo, host = get_default_ifo()
    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('files', type=Path, nargs='*', help='List of files to print. If empty search for latest')
    parser.add_argument('-i', '--ifo', default=ifo, help='Which ifo\'s config file to use if files not specified')
    parser.add_argument('--reset', action='store_true',
                        help='Reset the segment_to_process.txt file so that the next run starts 30 minutes ago')
    parser.add_argument('--reset-period', type=int, default=1800,
                        help='How long to reset segments, in seconds.')

    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    files = args.files
    ifo = args.ifo
    if len(files) == 0:
        config = get_default_config(ifo)
        groups = list(config.sections())
        groups.sort()
        online_dir = Path(f'{os.getenv("HOME")}/omicron/online/')
        for group in groups:
            file = online_dir / f'{ifo[0]}-{group}' / 'segments.txt'
            if file.exists():
                files.append(file)

    seg_pat = re.compile('\\d+\\s+(\\d+)\\s+(\\d+)\\s+(\\d+)')
    now = tconvert(tconvert())
    now_gps = int(tconvert())
    reset_period: int = args.reset_period
    reset_time: int = now_gps - 1800
    reset: bool = args.reset
    reset_files = list()

    for file in files:
        file = Path(file)
        if not file.exists():
            logger.critical(f'file : {file.absolute()} does not exist')
            continue
        with file.open('r') as infp:
            line = infp.readline()
            while line:
                m = seg_pat.match(line)
                if m:
                    s = int(m.group(1))
                    s_str = tconvert(s)
                    e = int(m.group(2))
                    e_str = tconvert(e)
                    end_dt = from_gps(e)
                    d = int(m.group(3))
                    dt = timedelta(seconds=d)
                    fn = str(file.parent.name) + '/' + str(file.name)
                    age = now - end_dt
                    if reset and e < reset_time:
                        reset_files.append(file)
                    print(f'{fn}: {s} - {e} : {s_str} - {e_str} ({d} s, {str(dt)}) to now: {str(age)}')
                line = infp.readline()
    hdr = '# seg    start         stop          duration'
    for file in reset_files:
        with file.open('w') as outfp:
            dt = float(reset_period)
            line = f'{hdr}\n0        {reset_time - 900:10d}    {reset_time:10d}   {dt:7.1f}'
            print(f'{file.absolute()}:\n{line}')
            print(line, file=outfp)

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()
