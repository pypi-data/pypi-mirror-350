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
Scan trigger directories to create bash scripts to create tar
files for each channel covering a time interval
"""

import time

from gwpy.time import to_gps
from ligotimegps import LIGOTimeGPS

from omicron_gap.gap_utils import get_default_ifo

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None
ifo, host = get_default_ifo()


def parser_add_args(parser):
    """
    Set up command parser
    :param argparse.ArgumentParser parser:
    :return: None but parser object is updated
    """
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')

    default_indir = Path('home/detchar/triggers') / ifo if ifo is not None else None
    parser.add_argument('-i', '--indir', type=Path, default=default_indir,
                        help='Input directory containing channel directories')
    parser.add_argument('-o', '--outdir', type=Path, help='Where to store tar files')

    parser.add_argument('times', type=to_gps, nargs='+',
                        help='Time range [start, end) to process. may be 4-5digit "metric day", GPS time or date/time')


def main():
    global logger

    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_add_args(parser)
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

    indir: Path = args.indir
    outdir: Path = args.outdir
    outdir.mkdir(mode=775, parents=True, exist_ok=True)
    strt_gps: LIGOTimeGPS = args.times[0]
    end_gps: LIGOTimeGPS = args.times[1]
    strt_dir = int(strt_gps.gpsSeconds / 100000)
    end_dir = int(end_gps.gpsSeconds / 100000)

    tarfile = outdir / f'tarcmd-{strt_dir:05d}-{end_dir:05d}.sh'

    channels = list(indir.glob('*'))
    logger.info(f' {len(channels)} file/directories found in {indir.absolute()}')
    with tarfile.open('w') as tfp:
        print('#!/bin/bash', file=tfp)
        if len(channels) > 0:
            channels.sort()
        n_chan = 0
        n_tdirs = 0
        chan: Path
        for chan in channels:
            if chan.is_dir():
                n_chan += 1
                time_dirs = chan.glob('*')
                chan_dirs = list()
                for tdir in time_dirs:
                    if tdir.is_dir():
                        name = tdir.name
                        m = re.match('(\\d+)', name)
                        if m:
                            dir_time = int(m.group(1))
                            if strt_dir <= dir_time < end_dir:
                                chan_dirs.append(tdir)
                                n_tdirs += 1
                        logger.debug(f'{tdir.name} has {len(chan_dirs)} matching dirs')
                if len(chan_dirs) > 0:
                    pass    # not implemented yet


if __name__ == "__main__":

    main()
    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
