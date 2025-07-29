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

"""Part of gap handler Condor, this is used as a post script after multiple
pyomicron jobs have created DAGs. This creates a subdag descriptor
to run them a fixed number at a time"""

import time
from pathlib import Path
from gpstime import tconvert

start_time = time.time()
import argparse
import logging
from ._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'gap-subdag-create'


def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__,
                                     prog=__process_name__)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-i', '--inpath', type=Path, required=True,
                        help='Template for directories created by pyomicron')
    parser.add_argument('-o', '--outpath', type=Path, required=True,
                        help='path to output dag')
    parser.add_argument('-g', '--group', help='Group which leads subdir names')
    parser.add_argument('-n', '--njobs', default=8, type=int,
                        help='how many dags to run in parallel')

    args = parser.parse_args()

    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    outpath: Path = args.outpath
    outpath.parent.mkdir(0o755, parents=True, exist_ok=True)
    log_file = outpath.parent / 'gap_subdag_create.log'
    log_file.parent.mkdir(0o755, parents=True, exist_ok=True)

    fhandler = logging.FileHandler(log_file, mode='a')
    if logger.level < logging.INFO:
        log_format = "%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
    else:
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)

    for k, v in vars(args).items():
        if k == 'start' or k == 'end':
            s = f', ({tconvert(v)})'
        else:
            s = ''
        logger.debug(f'arg: {k} = {v}{s}')

    dag_pat = f'{args.group}*/condor/*.dag'
    dag_list = list(Path(args.inpath).glob(dag_pat))

    if len(dag_list) == 0:
        logger.info(f'we have no dags to process in {args.inpath}')
    else:
        outdag = Path(outpath)
        logger.info(f'There are {len(dag_list)} entries for the subdag in {outdag}')
        group = args.group
        njobs = args.njobs

        with outdag.open('w') as outfp:
            for n in range(0, len(dag_list)):
                subdag_name = f'{group}_{n:02d}'
                logger.info(f'{subdag_name} {dag_list[n]}')
                print(f'SUBDAG EXTERNAL {subdag_name} {dag_list[n]}', file=outfp)

            if len(dag_list) > njobs:
                print('CATEGORY ALL_NODES LIMIT', file=outfp)
                print(f'MAXJOBS LIMIT {njobs}', file=outfp)

    elap = time.time() - start_time
    logger.info('run time {:.1f} s'.format(elap))


if __name__ == "__main__":
    main()
