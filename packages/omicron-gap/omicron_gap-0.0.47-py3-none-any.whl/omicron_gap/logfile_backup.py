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
Backup (tar) and delete old log files
"""
import datetime
import os
import shutil
import time

import pytz

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
import subprocess
from ._version import __version__


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'omicron-gap'


def run_cmd(cmd, logger):
    ret = 0
    try:
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0:
            logger.critical(f'{cmd[0]} returned {r.returncode}\n'
                            f'{r.stdout.decode("utf-8")}\n\n{r.stderr.decode("utf-8")}')
            ret = r.returncode
    except ValueError as ex:
        logger.critical(f'Exception caught running {cmd[0]}: {ex}')
        ret = 2
    return ret


def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    # defaults
    base_dir = Path.home() / 'omicron' / 'online'

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('basedir', type=Path, default=base_dir, nargs='*', help='Where to look for log file directory')
    parser.add_argument('--dry-run', action='store_true', help='Log but do not execute commands')

    parser.epilog = """Find log file directories older than 9 weeks, tar the directories and remove them"""

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

    now = datetime.datetime.now(pytz.UTC)
    td = datetime.timedelta(weeks=9)

    basedirs = args.basedir if isinstance(args.basedir, list) else [args.basedir]

    for bdir in basedirs:
        basedir = Path(bdir)
        files = basedir.glob('*/20*')
        start_dir = Path.cwd()

        for file in files:
            name = file.name
            if file.is_dir() and re.match('^\\d+', name) and len(name) == 6:

                year = int(name[0:4])
                mon = int(name[4:6])
                dir_date = datetime.datetime(year=year, month=mon, day=1, tzinfo=pytz.UTC)

                os.chdir(file.parent)
                backup_dir = file.parent / "log-backups"
                backup_dir.mkdir(0o775, exist_ok=True)
                logger.info(f'Backup dir: {file.absolute()}')

                # check for old backups
                old_backups = list(file.parent.glob('*tgz'))
                for bkup in old_backups:
                    logger.info(f'old backup found {bkup.absolute()}, moving to {str(backup_dir)}')
                    if not args.dry_run:
                        shutil.move(bkup, backup_dir)

                dir_age = now - dir_date
                if dir_age > td:
                    proc_start = time.time()
                    tar_file = backup_dir / f'{name}.tgz'
                    tar_cmd = ['tar', '-czf', str(tar_file.absolute()), name]
                    logger.info(f'    cd {file.parent}')
                    logger.info(f'    {" ".join(tar_cmd)}')
                    rm_cmd = ['rm', '-rf', str(file.absolute())]
                    logger.info(f'    {" ".join(rm_cmd)}')
                    if not args.dry_run:
                        if run_cmd(tar_cmd, logger) != 0:
                            continue
                        run_cmd(rm_cmd, logger)
                        os.chdir(start_dir)

                    logger.info(f'Processed {file.name} took {time.time() - proc_start:.1f}s')

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    curdir = Path.cwd()
    main()
    os.chdir(curdir)
