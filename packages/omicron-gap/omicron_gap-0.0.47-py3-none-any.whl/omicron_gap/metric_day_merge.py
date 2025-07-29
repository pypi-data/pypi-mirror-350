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

"""Online Omicron produces a lot of files, this program goes through all channels for
a metric day: int(GPS/100000) to merge any contiguous files into a new indir"""

import shutil
import subprocess
import sys
import time
import socket
from pathlib import Path

from gwpy.time import to_gps

start_time = time.time()
import argparse
import glob
import logging

import os
import htcondor  # for submitting jobs, querying HTCondor daemons, etc.
from ._version import __version__


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'metric_day_merge'

exts = ['h5', 'root', 'xml.gz']
merge_cmd = 'omicron-batch-merge-dir'

log_format = "%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format)
formatter = logging.Formatter(log_format)
logger = logging.getLogger(__process_name__)
logger.setLevel(logging.DEBUG)


def get_exe(prog_name):
    ret = shutil.which(prog_name)

    if ret is None:
        path_guess = Path(sys.executable).parent / prog_name
        if path_guess.exists():
            ret = str(path_guess.absolute())
    return ret


def process_dir(indir, outdir, logger, ext):
    """

    @param Path indir: directory to scan: <base>/<chan>/<day>
    @param Path outdir: new base directory for merged files
    @return:
    """
    thedir = Path(indir)
    chan_tag = thedir.parent.name
    day = thedir.name
    outpath = outdir
    layers = list()
    trg_files = glob.glob(f'{str(thedir)}/*.{ext}')
    logger.info(f'{len(trg_files)} {ext} files to merge in {chan_tag}')
    if len(trg_files) > 0:

        layer = {'cmd': merge_cmd,
                 'outdir': outpath,
                 'chan': chan_tag,
                 'day': day,
                 'ext': ext
                 }
        layers.append(layer)
    return layers


def main():
    global merge_cmd

    host = socket.getfqdn()
    if 'ligo-la' in host:
        ifo = 'L1'
    elif 'ligo-wa' in host:
        ifo = 'H1'
    else:
        ifo = None

    def_dir = f'/home/detchar/triggers/{ifo}' if ifo else None

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     prog=__process_name__)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-i', '--ifo', default=ifo, help='Specify IFO if not implied from hostname ')
    parser.add_argument('-t', '--trig-dir', default=def_dir,
                        help='Base directory for search ')
    parser.add_argument('-o', '--outdir', required=True, help='path for output files and directories')
    parser.add_argument('-d', '--day', type=to_gps, help='metric day, gps, or date')
    parser.add_argument('-e', '--ext', help='Extension (root, h5, xml) (default: all)')
    parser.add_argument('--njobs', type=int, default=8, help='Number of parallel condor jobs. ')
    parser.add_argument('--submit', action='store_true', help='Submit the condor job')
    parser.add_argument('--channel', help='Single channel to process, debugging')
    parser.add_argument('-l', '--logfile', type=Path, help='File to append log messages')

    args = parser.parse_args()

    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    if args.logfile:
        args.logfile.parent.mkdir(mode=0o755, exist_ok=True, parents=True)

        handler = logging.handlers.RotatingFileHandler(args.logfile.absolute(), maxBytes=(1048576 * 5), backupCount=4)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.debug('{} called with arguments:'.format(__process_name__))
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    trig_dir = None
    err = list()
    if args.trig_dir:
        trig_dir = args.trig_dir
    elif args.ifo:
        trig_dir = f'/home/detchar/triggers/{args.ifo}'
    if trig_dir:
        trig_dir = Path(trig_dir)
        if not trig_dir.is_dir():
            err.append(f'Trigger directory ({trig_dir.absolute()} does not exist or is not a directory')
    else:
        err.append('trigger directory (--trig-dir) or IFO (--ifo) must be '
                   'specified if not running in an IFO cluster')

    logger.debug(f'Input trigger directory: {trig_dir}')

    if args.day:
        day = args.day if args.day < 1e6 else int(args.day / 1e5)
    else:
        err.append('Metric day to scan must be specified')

    if not args.outdir:
        err.append('Output directory must be specified')
    outdir = Path(args.outdir)

    default_cmd = 'omicron-batch-merge-dir'
    merge_cmd = get_exe(default_cmd)
    if merge_cmd is None:
        err.append(f'Program {default_cmd} not found')
    else:
        logger.debug(f'Using {merge_cmd}')

    channel = args.channel if args.channel else '*'

    if err:
        print('\n'.join(err), file=sys.stderr)
        parser.print_help(file=sys.stderr)
        sys.exit(2)

    dir_cmds = list()
    dir_pat = str(trig_dir / channel / str(day))

    logger.info(f'Search pattern: {dir_pat}')
    dirs = glob.glob(dir_pat)
    dirs.sort()
    logger.info(f'{len(dirs)} channels found.')
    for idir in dirs:
        for ext in exts:
            cmds = process_dir(idir, outdir, logger, ext)
            if len(cmds) > 0:
                dir_cmds.extend(cmds)

    scripts = list()
    script_paths = list()
    njobs = args.njobs
    condor_dir = outdir / 'condor'
    condor_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    for n in range(0, njobs):
        scripts.append(list())
        script_path = condor_dir / f'merge_{n + 1:02d}.sh'
        script_paths.append(script_path)
    n = 0
    # distribute commands into the multiple scripts
    for cmd in dir_cmds:
        cmd_log = condor_dir / f'batch-merge-{cmd["chan"]}-{cmd["day"]}-{cmd["ext"]}.log'
        c = f'{cmd["cmd"]} -vvv --outdir {cmd["outdir"]} --logfile {cmd_log} --indir {str(trig_dir.absolute())} '
        c += f' --channel {cmd["chan"]} --day {cmd["day"]} --ext {cmd["ext"]}'
        scripts[n].append(c)
        n = n + 1 if n < njobs - 1 else 0

    # Write the script files
    for n in range(0, njobs):
        if len(scripts[n]) > 0:
            with script_paths[n].open(mode='w') as out:
                for c in scripts[n]:
                    print(f'{c}\n', file=out)

    # Write condor submit file
    try:
        user = os.getlogin()
    except OSError:
        user = 'joseph.areeda'

    submit = {'executable': shutil.which('bash'),
              'arguments': '$(script)',
              'accounting_group': 'ligo.prod.o3.detchar.transient.omicron',
              'accounting_group_user': 'joseph.areeda' if user == 'detchar' or user == 'root' else user,
              'request_disk': '1G',
              'request_memory': '1G',
              'getenv': 'True',
              'batch_name': 'Omicron day merge $(ClusterID)',
              'environment': '"HDF5_USE_FILE_LOCKING=FALSE"',
              'log': f'{str(condor_dir.absolute())}/merge.log',
              'error': '$(script).err',
              'output': '$(script).out',
              'notification': 'never',
              }

    submit_path = condor_dir / 'merge.sub'
    with submit_path.open(mode='w') as subfile:
        for k, v in submit.items():
            print(f'{k} = {v}', file=subfile)
        print(f'queue script matching files {str((condor_dir / "merge_*.sh").absolute())}', file=subfile)

    sub_obj = htcondor.Submit(submit)
    item_data = [{'script': str(path.absolute())} for path in script_paths]
    if args.submit:
        condor_start = time.time()
        schedd = htcondor.Schedd()
        submit_result = schedd.submit(sub_obj, itemdata=iter(item_data))
        cluster_id = submit_result.cluster()
        logger.info(f'Condor job submitted with JobID {cluster_id}')
        logger.info('Waiting for condor job to complete')
        wait_args = ['condor_watch_q', '-clusters', str(cluster_id), '-exit', 'all,done']
        res = subprocess.run(wait_args, stdout=subprocess.DEVNULL)
        condor_elap = time.time() - condor_start
        if res.returncode == 0:
            logger.info(f'Condor job completed with return code 0 in {condor_elap:.1f} s, see ready directory')
        else:
            logger.error(f'Condor returned with status {res.returncode} in {condor_elap:.1f} s')
    else:
        logger.info(f'To run under condor:\n condor_submit {submit_path.absolute()}')

    logger.info(f'output located in {outdir.absolute()}')

    elap = time.time() - start_time
    logger.info('run time {:.1f} s'.format(elap))


if __name__ == "__main__":
    main()
