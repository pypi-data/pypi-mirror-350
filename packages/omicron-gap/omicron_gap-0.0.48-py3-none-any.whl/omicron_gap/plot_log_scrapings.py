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

""""""
import os
import time
from math import sqrt

import numpy as np
from omicron_utils.histogram_plot import histogram_plot

start_time = time.time()

import argparse
import logging
from pathlib import Path
import sys
import traceback

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None


def hist_plot_column(data, col_name, title_name, out_dir, out_name):
    """
    Plot a histogram of a specific (numeric) column from a numpy data table
    :param numpy.ndarray data: full data table
    :param str col_name: which column to plot
    :param str title_name: how to refer to column in plot's super title
    :param Path | str out_dir: path to directory to write plot
    :param str out_name: how to refer to column in output file (no spaces please)
    :return Path: output file path
    """
    pctls = [0, 25, 50, 75, 90, 95, 98, 100]

    column_raw_data = data[:][col_name]
    if len(column_raw_data) > 0:
        column_data = column_raw_data[np.isfinite(column_raw_data)]
        plot_title = f'{title_name}, jobs: {len(column_data)} jobs out of {len(column_raw_data)}'
        logger.info(plot_title)
        for pct in pctls:
            percentile = np.percentile(column_data, pct)
            print(f'{pct}%: {percentile:.1f}, ', end=' ')
            plot_title += r'$\bf{' f'{pct}' r'}$' f': {percentile:.1f}, '
        print('\n')
        # Plot histogram of process segment length
        plt_xmax = np.percentile(column_data, 98)
        nbins = int(min(plt_xmax, sqrt(len(column_data))))

        out_path = out_dir / f'{out_name}-histogram.png'
        histogram_plot(column_data, out_path, xscale='98%', bins=nbins,
                       title=plot_title, logger=logger)
        return out_path


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
    parser.add_argument('infiles', nargs='+', type=Path,
                        help='One or more CSV files from omicron-log-scanner')


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

    data = None
    tmpdir = os.getenv('TMPDIR')
    if tmpdir is None:
        tmpdir = Path.home() / 'joe' / 't'
    outdir = Path(tmpdir)

    for infile in args.infiles:
        outdir = Path(infile).parent
        atable = np.genfromtxt(infile, delimiter=',', names=True, autostrip=True, dtype=None,
                               encoding='utf-8')
        if data is None:
            data = atable
        else:
            data = np.hstack((data, atable))
    logger.info(f'Total jobs: {data.size}')

    column_names = data.dtype.names

    if 'Qtime' in column_names:
        local_jobs = data[data[:]['Local'] == 1]
        vanilla_jobs = data[data[:]['Local'] == 0]

        # percentiles
        for jobls, lst_name in [(local_jobs, 'local'), (vanilla_jobs, 'vanilla')]:
            hist_plot_column(jobls, "Qtime", f'{lst_name}-queue', outdir, f'{lst_name}-queue')

    if 'FrameAge' in column_names:
        hist_plot_column(data, 'FrameAge', 'Frame age seconds', outdir, 'frame-age', )

    if 'want_seg_len' in column_names:
        hist_plot_column(data, 'want_seg_len', 'Segment length to process', outdir, 'wantseg-len')

    if 'Missing' in column_names:
        hist_plot_column(data, 'Missing', 'Missing triggers (s)', outdir, 'missing')

    count_columns = ['Too_short', 'Stalled', 'Valid', 'No_analyzable', 'Nomicron_jobs']
    for count_col in count_columns:
        if count_col in column_names:
            col_data = data[count_col]
            n = np.count_nonzero(col_data)
            logger.info(f'{count_col}: {n} out of {data.size}')


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
