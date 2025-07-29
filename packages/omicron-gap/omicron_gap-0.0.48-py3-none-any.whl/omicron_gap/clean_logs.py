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
Scan the online and gap filling log directories to remove old trigger files
"""
import datetime
import time

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
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
default_dirs = [Path.home() / 'omicron']


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

    parser.add_argument('search_dirs', type=Path, nargs='*', default=default_dirs,
                        help='One or ,ore top level directories to check')
    parser.add_argument('--age', default='1.5d',
                        help='Ninimum age for ddeletions seconds or <number<unit> units=m[inutes], h[ours], d[ays], '
                             'weeks')
    parser.add_argument('--test', action='store_true', help='Log but do not delete eligible files')


class CleanLogs:
    """
    methods to find and delete unneeded trigger files from failed Condor jobs
    """
    def __init__(self, age, test, logger):
        """

        :param int age: mi imum age to delete in seconds
        :param bool test: log but don't delete elegible files
        :param logging.Logger logger: program's logger
        """
        self.age = age
        self.test = test
        self.logger = logger
        self.ndirs = 0
        self.nfiles = 0
        self.ndel = 0
        self.nbytes = 0
        self.nblocks = 0
        self.ndir_del = 0
        self.now = datetime.datetime.utcnow()

    def proc_dir(self, indir):
        """
        walk directory tree looking for eligible trigger files
        :param Path indir: top level directory for search (reentrant)
        :return:
        """
        logger.debug(f'Scanning directory {indir.absolute()}')
        self.ndirs += 1
        files = list(indir.glob('*'))
        if files:
            for file in files:
                if file.is_symlink():
                    pass
                if file.is_dir():
                    self.proc_dir(file)
                elif file.is_file():
                    self.proc_file(file)
        else:
            tst_str = 'Would delete' if self.test else 'Delete'
            logger.debug(f'{tst_str} empty directory {indir.absolute()}')
            self.ndir_del += 1
            if not self.test:
                indir.rmdir()

    def proc_file(self, file):
        """
        check if file meet criteria for deletion
        :param  Path file:
        :return: None
        """
        if re.match('.*h5$|.*root$|.*xml$|.*xml.gz$', file.name):
            self.nfiles += 1
            fstat = file.stat()
            mtime = fstat.st_mtime
            file_age = self.now - datetime.datetime.utcfromtimestamp(mtime)
            if file_age.total_seconds() > self.age:
                self.ndel += 1
                tst_str = 'Would delete' if self.test else 'Delete'
                logger.debug(f'{tst_str} {file.absolute()},{fstat.st_size / 1e6:.2f}MB ')
                self.nbytes += fstat.st_size
                if not self.test:
                    file.unlink()


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

    if args.age:
        m = re.match('^([\\d.]+)([hdwmHDWM]\\w*)', args.age)
        if m:
            age = float(m.group(1))
            period = m.group(2)[0]
            period = period.lower()

            if period == 'h':
                age *= 3600
            elif period == 'd':
                age *= 86400
            elif period == 'w':
                age *= 86400 * 7
            elif period != 'm':
                raise ValueError(f'Unknown units for age [{m.group(2)}]')
        else:
            raise ValueError(f'Invalid age [{args.age}]')
    else:
        age = 1.5 * 24 * 3600

    cleaner = CleanLogs(int(age), args.test, logger)
    for indir in args.search_dirs:
        cleaner.proc_dir(indir)

    wouldbe = 'would be ' if args.test else ''
    logger.info(f'{cleaner.ndirs} directories, {cleaner.nfiles} files seen. {cleaner.ndel} files {wouldbe}deleted,\n'
                f' {cleaner.ndir_del} empty directories, file size {cleaner.nbytes / 1e9:.2f}GB, space recovered '
                f'{cleaner.nblocks / 1e9:.2f}GB ')


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
