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

"""Examine directories with files named as "<chan id>-<start gps>-<duration>.<ext>"
create a CSV and histogram plot of latency defined as <file last modification>-<start+dur>
NB: use gwf for frames h5, xml.gz or root for omicron triggers
"""

import time
import traceback
from datetime import datetime
from math import sqrt

import pytz
from gwdatafind import find_urls
from gwpy.timeseries import TimeSeries

from omicron_gap.gap_utils import get_default_ifo, gps2utc

start_time = time.time()

import argparse
import logging
import numpy as np
import os
from pathlib import Path
import re
import sys

from gwpy.time import to_gps, tconvert, Time
from matplotlib import use, pyplot
use('agg')

# globals

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(sys.argv[0]).stem
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

logging.basicConfig()
logger = logging.getLogger(__process_name__)
logger.setLevel(logging.DEBUG)


global time_pat, mingps, frnames
frnames: set

# if launched from a terminal with no display
# Must be done before modules like pyplot are imported
if len(os.getenv('DISPLAY', '')) == 0:
    use('Agg')


def get_frame_end(frame_uri):
    global mingps
    end = None
    m = time_pat.match(str(frame_uri))
    if m:
        frnames.add(m.group(1))
        st = int(m.group(2))
        mingps = min(st, mingps)
        dur = int(m.group(3))
        end = st + dur
    return end


def get_age(path, csvfp):
    endgps = get_frame_end((path.absolute()))
    try:
        enddate = Time(endgps, format='gps', scale='utc').datetime
        enddate = enddate.replace(tzinfo=pytz.UTC)
        lastmod = datetime.fromtimestamp(path.stat().st_mtime, pytz.UTC)
        age = (lastmod - enddate).total_seconds()
        if csvfp is not None:
            print(f'{age:.1f}, "{path.absolute()}", {endgps}, {enddate.strftime("%x %X")}, '
                  f'{lastmod.strftime("%x %X")}', file=csvfp)
    except (FileNotFoundError, ValueError):
        # happens with /dev/shm
        age = -1
    return age, endgps


def plot_res(ages, outbase, suptitle='', title='', xscale=None, bins=None):
    outpng = Path(outbase + '-histogram.png')

    # plot histogram
    xmin = ages.min()
    xmax = ages.max()
    if xscale:
        if '%' in xscale:
            pct = float(xscale.replace('%', ''))
            plt_xmax = np.percentile(ages, pct)
        else:
            plt_xmax = float(xscale)
    else:
        plt_xmax = xmax
    logger.info(f'Plot max: {plt_xmax:.1f}')
    new_ages = ages[ages <= plt_xmax]
    nbins = bins if bins else int(max(10, round(sqrt(len(new_ages)))))
    logger.info(f'nbins: {nbins}')
    pyplot.hist(new_ages, nbins)
    fig = pyplot.gcf()
    fig.set_size_inches(16, 10)
    ax = pyplot.gca()
    if suptitle:
        pyplot.suptitle(suptitle)
    if title:
        ax.set_title(title, fontsize=10, y=.97)
    ax.set_xlabel('Time (s) last gps to file write')
    ax.set_ylabel('N')

    ax.set_xlim(xmin, plt_xmax)
    pyplot.savefig(outpng)
    logger.info(f'Saved histogram as: {str(outpng.absolute())}')


def plot_ts(t, latency, outbase, title, summary):
    tmp = np.column_stack((t, latency))
    sorted_input = tmp[tmp[:, 0].argsort()]
    ts = TimeSeries(sorted_input[:, 1], name='Latency', unit='s', times=sorted_input[:, 0])
    out_file = Path(outbase + '-latency.png')
    plot = ts.plot(figsize=[16.0, 10.0], dpi=100)
    plot.suptitle(title, y=.97)
    ax = plot .gca()
    ax.set_title(summary, y=.94)
    plot.savefig(out_file)
    logger.info(f'Latency time series plot written to {out_file.absolute()}')


def main():
    global time_pat, mingps, frnames
    time_pat = None
    mingps = tconvert()
    frnames = set()

    ifo, host = get_default_ifo()

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('dir', type=Path, help='one or more files or directories to examine ', nargs='*')
    parser.add_argument('-o', '--outbase',
                        help='Path and base for output csv, plot. eg: ~/t/H1_R produces '
                             'files named H1_R-tme.csv and H1_R.png')
    parser.add_argument('-e', '--ext', default='gwf', help='file extension (no dot) '
                                                           'must follow *-<start gps>-<dur>.<ext>')
    parser.add_argument('--xmax', help='Scale plot x-axis. Append %% to specify as percentile 0-100)')
    parser.add_argument('--title', help='Graph super title')
    parser.add_argument('--bins', type=int, help='Override default number of bins in the histogram')

    parser.add_argument('--ifo', default=ifo, help='Specify IFO if not at a LIGO cluster')
    parser.add_argument('--frame-type', help='Do not include IFO ffor example L1_R')
    parser.add_argument('--gps', type=to_gps, nargs=2, help='Start, stop gps or datetime')

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

    ext = args.ext
    time_pat = re.compile(f'(.*)-(\\d+)-(\\d+)\\.{ext}')

    res = []
    gps_times = []

    suptitle = ''
    if args.outbase:
        outcsv = Path(args.outbase + '-times.csv')
        outcsv.parent.mkdir(parents=True, exist_ok=True)
        csvfp = outcsv.open('w')
        print('Age(s), File, End-GPS, End date/time, Last Modified', file=csvfp)
        logger.info(f'CSV data written to {str(outcsv.absolute())}')
    else:
        csvfp = None

    for d in args.dir:
        parent_dir = Path(d).parent
        globs = parent_dir.glob(d.name)
        flist = []
        for p in globs:
            if p.is_dir():
                suptitle += ', ' if suptitle else ''
                suptitle += p.name
                g_pat = f'*.{ext}'
                cur_list = list(p.glob(g_pat))
                logger.debug(f'{len(cur_list)} files found in {p.absolute()}')
                flist.extend(cur_list)
            f: Path | str
            for f in flist:
                age, egps = get_age(Path(f), csvfp)
                if age >= 0:
                    res.append(age)
                    gps_times.append(egps)
    if args.frame_type and args.gps:
        obs = args.ifo[0]
        ftyp = args.frame_type
        strt = args.gps[0]
        stop = args.gps[1]
        logger.info(f'findurls({obs}, {ftyp}, {gps2utc(strt)}, {gps2utc(stop)}')
        flist = find_urls(args.ifo[0], args.frame_type, args.gps[0], args.gps[1])
        for f in flist:
            path = Path(f.replace('file://localhost', ''))
            age, egps = get_age(path, csvfp)
            if age >= 0:
                res.append(age)
                gps_times.append(egps)

    ages = np.asarray(res)
    n_samples = ages.size
    maxgps = 0
    if n_samples > 0:
        maxgps = max(gps_times)

        mean = ages.mean()
        qtiles = 'Quartiles: '
        for q in [0, 25, 50, 75, 90, 95, 97, 99, 100]:
            qtile = np.percentile(ages, q)
            qtiles += r'$\bf{' f'{q}' r'}$' f': {qtile:.1f}, '

        summary = f'N: {n_samples}, Mean: {mean:.2f} {qtiles}\n\n'
        logger.info(summary)
        if args.outbase:
            if args.title:
                suptitle = args.title
            else:
                frn = list(frnames)
                suptitle = frn[0] if len(frn) > 0 else ''
                suptitle += ' ... ' if len(frn) > 1 else ''
                suptitle += f' {mingps} - {maxgps} ({gps2utc(mingps)} - {gps2utc(maxgps)}'
            plot_res(ages, args.outbase, suptitle, summary, args.xmax, args.bins)
            plot_ts(gps_times, res, args.outbase, suptitle, summary)
    else:
        print('No appropriate files found.\n')
    csvfp.close()
    logger.info(f'Elapsed time {time.time() - start_time:.1f}s')


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
