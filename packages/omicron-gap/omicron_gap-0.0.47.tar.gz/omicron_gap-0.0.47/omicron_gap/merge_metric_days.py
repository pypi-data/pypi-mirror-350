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
To address the large number of omicron trigger file, this program wrap several omicron utilities to merge
contiguous trigger files in one metric day (GPS/100000)
"""
import shutil
import time

from omicron_gap.gap_utils import get_default_ifo

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
import subprocess
import sys
from ._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'merge-metric-days'


def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    ifo, host = get_default_ifo()
    logger.debug(f'hostname: {host} Default IFO: {ifo}')

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')

    parser.add_argument('-i', '--ifo', required=(ifo is None), default=ifo,
                        help='Needed only if it cannot be determined automatically')
    parser.add_argument('-c', '--chan', type=Path,
                        help='Path to the channel directory that contains metric day directories.')
    parser.add_argument('day', nargs='+', help='Metric day or start, end date')
    parser.add_argument('-o', '--outbase', type=Path, required=True, help='Base directory for output files')
    parser.add_argument('--nosubmit', action='store_true', help='Do not submit jobs to condor. '
                                                                'NB condor submit files will be created')
    parser.add_argument('--noupdate', action='store_true', help='Do not update the "production" directories.')
    parser.add_argument('--test', action='store_true', help='Do not run the merge day program but log its command')
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

    mergedFlag = 'day_was_merged'

    ifo = args.ifo
    got_error = False
    if ifo is None:
        logger.error('Ifo cannot be determined automatically, it must be specified.')
        got_error = True

    if args.chan:
        chandir = Path(args.chan)
        if not chandir.is_dir():
            logger.error(f'Channel directory {chandir.absolute()} does not exist')
            got_error = True
        chan = chandir.name
    else:
        chan = None
    days = args.day
    outbase = Path(args.outbase)
    outbase.mkdir(mode=0o755, exist_ok=True, parents=True)
    omdm = shutil.which('omicron-metric-day-merge')
    if omdm is None:
        logger.error('omicron-metric-day-merge program not found.')
        got_error = True

    if got_error:
        sys.exit(1)

    if len(args.day) == 2:
        days = list()
        dayglob = chandir.glob('*')
        for d in dayglob:
            m = re.match('(\\d+)', d.name)
            if m:
                day = m.group(1)
                if args.day[0] <= day <= args.day[1]:
                    days.append(day)
    days.sort(reverse=True)

    for day in days:
        mflg_path = chandir / day / mergedFlag
        if (mflg_path).exists():
            logger.info(f'Day: {day}, chan: {chan} has already been processed.')
            continue

        outdir = outbase / chan / day
        outdir.mkdir(mode=0o755, exist_ok=True, parents=True)

        logfile = outdir / 'merge.log'
        cmd = [omdm, '-vvv', '--logfile', str(logfile.absolute()), '--channel', chan, '--day', day,
               '--outdir', str(outdir.absolute()), '--ifo', ifo]
        if not args.nosubmit:
            cmd.append('--submit')

        cmd_str = " ".join(cmd)
        logger.info(f'merge command:\n{cmd_str}')
        if not args.test:
            res = subprocess.run(cmd)
            logger.info(f'merge command returned {res.returncode}')
            fail_dir = outdir / 'failure'
            if fail_dir.exists():
                logger.error(f'Failures noted in {fail_dir.absolute()}')
            elif not args.nosubmit:
                cpycmds = (outdir / 'ready').glob('*copy.sh')
                for cpycmd in cpycmds:
                    cmd = ['bash', '-c', f'source {cpycmd.absolute()}']
                    cmd_str = " ".join(cmd)
                    if args.noupdate:
                        logger.info(f'To update run {cmd_str}')
                    else:
                        logger.info(f'running {cmd_str}')
                        subprocess.run(cmd)
                setflg = outdir / 'ready' / 'add_dir_processed_flag.sh'
                if setflg.exists():
                    set_cmd = ['bash', '-c', f'source {setflg.absolute()}']
                    set_str = " ".join(set_cmd)
                    if args.noupdate:
                        logger.info(f'To mark directory done run {set_str}')
                    else:
                        logger.info(f'running {set_cmd}')
                        subprocess.run(set_cmd)

    # report our run time
    logger.info(f'merge-metric-days: elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()
