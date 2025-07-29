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

""""""
import os
import sys
import time
import traceback
from math import floor, ceil

import gwtrigfind as gwtrigfind
from gwpy.table import EventTable
from gwpy.time import to_gps
import numpy as np

from omicron_gap.gap_utils import read_trig_list

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
from ._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'trigger_plot                  '

logging.basicConfig()
logger = logging.getLogger(__process_name__)
logger.setLevel(logging.DEBUG)


def read_trig_file(inpath):
    """
    Read a EventTable trigger file. Handle the formats h5, ligolw, and root
    :param Path inpath: path-like to trigger file
    :return EventTable: trigger read
    """
    table = EventTable()
    path = Path(inpath)

    if path.exists():
        if path.name.endswith('.h5'):
            try:
                table = EventTable.read(path, path='/triggers')
            except OSError:
                table = EventTable.read(path, path='/__astropy_table__')
        elif path.name.endswith('.xml.gz') or path.name.endswith('.xml'):
            table = EventTable.read(path, tablename='sngl_burst')
        elif path.name.endswith('.root'):
            # reading root files fail if there is a : in the name
            cwd = Path.cwd()
            os.chdir(path.parent)
            table = EventTable.read(str(path.name), treename='triggers;1')
            os.chdir(cwd)
    return table


def main():
    global logger

    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)

    epilog = """
    To plot omicron triggers for a channel specify channel name, xmin, and xmax for times; Or example:
    --channel H1:GDS_CALIB_STRAIN_NOLINES --xmin 12/10/24 --xmax 12/11/2024
    xmin and xmax can be gps, a date or date/time
    """
    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__, epilog=epilog,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-o', '--out', type=Path, help='Output file, substitute %%g with time range')
    display_group = parser.add_argument_group('display group', 'Plot customization parameters')
    display_group.add_argument('--xmin', type=to_gps, help='Plot minimum time, date/time, gps, offset if < 1000')
    display_group.add_argument('--xmax', type=to_gps, help='Plot maximum time, date/time, gps, offset if < 1000')
    display_group.add_argument('--epoch', type=to_gps, help='Plot maximum time, date/time, gps, offset if < 1000')
    display_group.add_argument('--ymin', type=float, help='Frequency axis minimum, default=auto')
    display_group.add_argument('--ymax', type=float, help='Frequency axis maximum, default=auto')
    display_group.add_argument('--cmin', type=float, default=0, help='Color bar axis minimum')
    display_group.add_argument('--cmax', type=float, default=25, help='Color bar axis maximum 0=auto')
    display_group.add_argument('--suptitle', help='Top title of plot')
    display_group.add_argument('--title', help='Axis title, 2nd line from top')
    display_group.add_argument('--geometry', default='10x6', help='wxh in inches (100dpi)')

    ingrp = parser.add_argument_group('Input specifier', 'Select one of the following')
    input_group = ingrp.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--trigfiles', nargs='+', type=Path, help='h5, ligolw or root trigger files')
    input_group.add_argument('--channel',
                             help='Channel name, requires --xmin and --xmax used as time range')
    parser.add_argument('--ext', default='h5', help='type of detchar trigger file (xml.gz, h5, root)')
    input_group.add_argument('--cache', type=Path, help='Path to file containing a list of paths to trigger files')
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

    trig_files = list()
    if args.trigfiles:
        trig_files = args.trigfiles
    elif args.channel:
        trig_files_uri = gwtrigfind.find_trigger_files(args.channel, 'omicron', args.xmin, args.xmax, ext=args.ext)
        trig_files = list()
        for tfile in trig_files_uri:
            tfile = re.sub('^file://', '', tfile)
            trig_files.append(Path(tfile))
    if trig_files is None or len(trig_files) == 0:
        logger.critical(f'No trigger files available for {args.channel} from {args.xmin}, {args.xmax}')
    trigs, channel, start, end = read_trig_list(trig_files)
    if trigs is None or len(trigs) == 0:
        logger.critical('No triggers found')
        exit(3)
    plot = trigs.scatter(trigs.colnames[0], trigs.colnames[1], color=trigs.colnames[2])
    ax = plot.gca()

    xmin = float(args.xmin) if args.xmin else trigs['time'].min() - 15
    xmin += start if xmin < 10000 else 0
    xmax = float(args.xmax) if args.xmax else trigs['time'].max() + 15
    xmax = end - xmax if xmax < 10000 else xmax
    ax.set_xlim(xmin, xmax)
    msk = np.logical_and(trigs['time'] >= xmin, trigs['time'] <= xmax)
    idx = trigs[msk]['snr'].argmax()
    max_evt = trigs[msk][idx]
    ax.scatter(max_evt['time'], max_evt['frequency'], marker='*', zorder=1000, facecolor='gold', edgecolor='black',
               s=200)
    if args.epoch:
        epoch = args.epoch if args.epoch > 10000 else start + args.epoch
        ax.set_epoch(float(epoch))
    ax.set_yscale('log')
    ax.set_ylabel('Frequency [Hz]')
    ymin = args.ymin if args.ymin else 10
    ymax = args.ymax if args.ymax else trigs['frequency'].max()
    ax.set_ylim(ymin, ymax)

    if args.title:
        title = args.title
    else:
        title = f"Star (max SNR) -> t: {max_evt['time']:.2f}, ƒ: {max_evt['frequency']:.1f} Hz, SNR:" \
                f" {max_evt['snr']:.1f}"
    ax.set_title(title, fontsize='medium')
    plot.colorbar(clim=[args.cmin, args.cmax], cmap='viridis', label='Signal-to-noise ratio (SNR)')

    if args.suptitle:
        suptitle = args.suptitle
    else:
        suptitle = channel
    plot.suptitle(suptitle, fontsize='large')

    out: Path = args.out
    if out.is_dir():
        outname = f'{channel}-{start}-{end - start}.png'
        out = out / outname
    else:
        outname = out.name
        time_spec = f'{floor(xmin)}-{ceil(xmax - xmin)}'
        outname = re.sub('%g', time_spec, outname)
        out = out.parent / outname

    m = re.match('([^xX]+)[xX](.+)', args.geometry)
    if m:
        try:
            w = float(m.group(1))
            h = float(m.group(2))
        except ValueError as ex:
            logger.critical(f'Invalid geometry {args.geometry}')
            raise ex
    else:
        raise ValueError(f'Invalid geometry {args.geometry}')
    plot.set_figwidth(w)
    plot.set_figheight(h)
    plot.savefig(out)
    plot.close()
    logger.info(f'Wrote {out.absolute()}')


if __name__ == "__main__":

    try:
        main()
    except (ValueError, TypeError, OSError, NameError, ArithmeticError, RuntimeError) as ex:
        print(ex, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        exit(10)
    except Exception as ex:
        print(f'Unknown exception {ex}', file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        exit(11)

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')
