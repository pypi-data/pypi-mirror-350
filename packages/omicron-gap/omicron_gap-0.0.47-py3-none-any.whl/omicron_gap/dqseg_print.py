#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2024 Joseph Areeda <joseph.areeda@ligo.org>
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
Commnd line segment printer
"""
import os
import time

from gwpy.time import to_gps, from_gps

from omicron_gap.gap_utils import get_default_ifo, get_gps_day

start_time = time.time()

import argparse
import logging
from pathlib import Path
import sys
import traceback

from gwpy.segments import DataQualityFlag


try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None

DEFAULT_SEGMENT_SERVER = os.environ.setdefault('DEFAULT_SEGMENT_SERVER', 'https://segments.ligo.org')
DEF_SEGMENTS = ['{ifo}:DMT-ANALYSIS_READY:1', '{ifo}:DMT-DC_READOUT_LOCKED:1', '{ifo}:DMT-GRD_ISC_LOCK_NOMINAL:1']

ifo, host = get_default_ifo()
def_segments = [item.replace('{ifo}', ifo) for item in DEF_SEGMENTS]
today = get_gps_day()[0]
tomorrow = get_gps_day()[1]


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

    parser.add_argument('-S', '--segments', nargs='*', default=def_segments,
                        help='One or more data quality segments')
    parser.add_argument('-i', '--ifo', default=ifo, type=str, help='IFO to use')
    parser.add_argument('-s', '--start', type=to_gps, default=today,
                        help='Start date/time, defaults to today')
    parser.add_argument('-e', '--end', type=to_gps, default=tomorrow,
                        help='End date/time, defaults to tomorrow')


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
        if k == 'start' or k == 'end':
            c = from_gps(v)
        else:
            c = ''
        logger.debug(f'    {k} = {v} {c}')

    os.unsetenv('HTTPS_PROXY')

    for segment in args.segments:
        seg_list = DataQualityFlag.query_dqsegdb(segment, args.start, args.end, url=DEFAULT_SEGMENT_SERVER)
        print(f'{segment}: {seg_list}')


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, OSError, NameError, ArithmeticError, RuntimeError) as ex:
        print(ex, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
