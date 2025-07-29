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
Manage availability plots to make an animated gif showing progress over a day
"""
import datetime
import time

from gpstime import tconvert
from gwpy.time import to_gps

from omicron_gap.gap_utils import get_default_ifo, get_gps_day, gps2dirname

start_time = time.time()

import argparse
import logging
from pathlib import Path
import subprocess
from ._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'gap_plot_animator'

ifo, host = get_default_ifo()
home = Path.home()
logger = None

std_segments = \
    [
        '{ifo}:DMT-GRD_ISC_LOCK_NOMINAL:1',
        '{ifo}:DMT-DC_READOUT_LOCKED:1',
        '{ifo}:DMT-CALIBRATED:1',
        '{ifo}:DMT-ANALYSIS_READY:1'
    ]
master_seg = '{ifo}:DMT-ANALYSIS_READY:1'


def get_day(st, en, yesterday):
    """
    Determine day start, end from command line args
    :param int|float|LIGOTimeGPS st: requested start time, None -> TODAY
    :param int|float|LIGOTimeGPS en: requested end time None -> start + 24hrs
    :param bool yesterday: use yesaterday from 00:00 UTC to TODAY 00:00
    :return tuple: start, end GPS as integer
    """
    if yesterday:
        start, end = get_gps_day(offset=-1)
    elif st:
        start, end = get_gps_day(st)
        if en:
            _, end = get_gps_day(en)
    else:
        start, end = get_gps_day()

    return start, end


def main():
    global logger

    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')

    parser.add_argument('start', type=to_gps, action='store', nargs='?', help='Start of plot, default=today 00:00 UTC')
    parser.add_argument('end', type=to_gps, action='store', nargs='?',
                        help='End of plot, end of day specified by start')
    parser.add_argument('--yesterday', action='store_true', help='set times to 24 hours covering yesterday')
    parser.add_argument('-E', '--epoch', type=float, action='store',
                        help='Delta < 10000000 or GPS', required=False)

    parser.add_argument('-i', '--ifo', type=str, default=ifo,
                        help='IFO (L1, H1, V1)')
    parser.add_argument('-l', '--log-file', type=Path, help='Save log messages to this file')
    parser.add_argument('-o', '--out', help='Base path to results: txt and png files. Default is '
                                            'a directory in ~/public_html/detchar-avail-mon based on month and day')
    parser.add_argument('-t', '--text', action='store_true', help='Save a text file of all data plotted')

    parser.add_argument('--std', action='store_true', help='Add "standard" segment list')
    parser.add_argument('-S', '--segments', type=str, nargs='*',
                        help='List of segments to examine with "{ifo}" ',
                        default=' '.join(std_segments))
    parser.add_argument('-g', '--geometry', help='Width x Height')
    parser.add_argument('--delay', type=int, default=30, help='Time between frames in output animation in 0.01s')
    parser.add_argument('-c', '--config', type=Path, help='omicron config default is to look in ~/omicron/online')

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

    start = args.start if args.start else tconvert()
    start, end = get_day(start, args.end, args.yesterday)
    mon, day = gps2dirname(start)

    plot_dir = Path.home() / 'public_html' / 'detchar-avail-anim' / mon / day
    plot_dir.mkdir(mode=0o775, parents=True, exist_ok=True)
    timestr = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%d-%H%M')
    plot_filename = f'{day}-{timestr}'
    plot_file = plot_dir / plot_filename

    plot_cmd = ['omicron-plot-gaps', '-vv', '--out', str(plot_file.absolute()), f'{int(start)}', f'{int(end)}']
    logger.info(f'Gap plot command:\n  {" ".join(plot_cmd)}')
    res = subprocess.run(plot_cmd, capture_output=True)
    if res.returncode != 0:
        logger.error(f'plot-gaps returned {res.returncode}\n{res.stderr.decode("utf-8")}')
    else:
        plot_files = list(plot_dir.glob('*.png'))
        plot_files.sort()

        animate_cmd = ['magick', '-delay', f'{args.delay}', '-loop', '0']
        for pf in plot_files:
            animate_cmd.append(str(pf.absolute()))
        animated_gif = plot_dir / f'{day}.gif'
        animate_cmd.append(str(animated_gif.absolute()))
        logger.info(f'Animate command:\n {" ".join(animate_cmd)}')
        res = subprocess.run(animate_cmd, capture_output=True)
        if res.returncode == 0:
            logger.info(f'animated availability written to {str(animated_gif.absolute())}')
        else:
            logger.error(f'animate gap plots (magick) returned {res.returncode}\n{res.stderr.decode("utf-8")}')


if __name__ == "__main__":
    main()
    # report our run time
    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
