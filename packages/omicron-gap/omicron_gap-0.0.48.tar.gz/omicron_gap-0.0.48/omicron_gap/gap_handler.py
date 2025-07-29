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

"""Manage  a fairly complicated set of DAGs to fill gaps if possible"""
import re
import subprocess
import sys
import time
import traceback

from omicron_utils.conda_fns import get_conda_run
from omicron_utils.omicron_config import OmicronConfig

from omicron_gap.gap_utils import get_default_ifo, get_gps_day, which_programs

start_time = time.time()

from logging.handlers import RotatingFileHandler

from pathlib import Path
import shutil

from gwpy.time import tconvert, to_gps, from_gps

from .Omicrondag import OmicronDag, OmicronTask, OmicronScript, OmicronSubdag
import argparse
import logging
import os
from ._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'gap-handler'

# global logger
log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
log_file_date_format = '%m-%d %H:%M:%S'
logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
logger = logging.getLogger(__process_name__)
logger.setLevel(logging.DEBUG)


def gps2str(gps):
    """Creat a string from gps time for filenames
    :param LIGOTimeGPS gps:
    :returns str: something like 20220726.193002
    """
    dt = tconvert(gps)
    ret = dt.strftime('%Y%m%d.%H%M%S')
    return ret


def check_x509():
    """Give us clear error messages for x509 issues"""
    ret = True
    gpi = shutil.which('ecp-cert-info')
    if gpi is None:
        logger.error('ecp-cert-info is not available')
        ret = False
    else:
        res = subprocess.run([gpi], capture_output=True)
        stdout = res.stdout.decode('utf-8')
        stderr = res.stderr.decode('utf-8')
        if res.returncode != 0:
            logger.error(f'ecp-cert-info returned {res.returncode} \n{stderr}')
            ret = False
        else:
            want_cert_types = ['end entity credential']
            cert_path = None
            for line in stdout.splitlines():
                m = re.match('^(type|path)\\s+:\\s+(.*)$', line)
                if m:
                    varname = m.group(1)
                    varval = m.group(2)
                    if varname == 'type':
                        got_cert_type = varval
                        if got_cert_type in want_cert_types:
                            logger.debug('Valid x509 certificate found.')
                        else:
                            logger.error(f'x509 certificate found but is not the expected type:\n '
                                         f'   Found: {got_cert_type}\n   Wanted: {want_cert_types}')
                            ret = False
                    elif varname == 'path':
                        cert_path = varval
            if ret and cert_path is not None:
                home = os.getenv('HOME')
                x509path = Path(f'{home}') / 'active_certificates' / 'x509.pem'
                cert_path = Path(cert_path)
                if x509path != cert_path and not x509path.exists():
                    if not x509path.parent.exists():
                        x509path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                    shutil.copy(cert_path, x509path)
                os.environ['X509_USER_PROXY'] = str(x509path.absolute())
                logger.debug(f'setting X509_USER_PROXY={os.getenv("X509_USER_PROXY")}')
                os.unsetenv('HTTPS_PROXY')
    return ret


def main():
    global logger
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    ifo, host = get_default_ifo()
    if ifo is None:
        logger.debug(f'Unable to determine ifo from {host}')

    home = Path.home()
    online_dir = home / 'omicron' / 'online'
    group_paths = online_dir.glob('*groups.txt')
    group_set = set()
    for group_path in group_paths:
        with open(group_path, 'r') as gpfp:
            grps = gpfp.read()
            for g in grps.splitlines():
                group_set.add(g)
    groups = list(group_set)
    groups.sort()

    me = Path(__file__)
    myname = me.name

    omicron_config = OmicronConfig(logger=logger)

    config = omicron_config.get_config()
    default_env = config['conda']['environment'] if config.has_option('conda', 'environment') else None
    conda_env = os.getenv('CONDA_PREFIX', default_env)
    if conda_env is None:
        logger.critical('Cannot determine conda environment')
        exit(10)

    csec = ", ".join(config.sections())
    logger.debug(f'My config sections: {csec}')
    if 'condor' in config.sections() and 'accounting_group_user' in config['condor']:
        acct_user = config['condor']['accounting_group_user']
    else:
        acct_user = os.getenv('USER')

    defmin = int(config['gap_handler']['min_gap']) if config.has_option('gap_handler', 'min_gap') else 128
    defmax = int(config['gap_handler']['max_gap']) if config.has_option('gap_handler', 'max_gap') else 7200
    defnjobs = int(config['gap_handler']['njobs']) if config.has_option('gap_handler', 'njobs') else 8
    output_dir_name = config['gap_handler']['output_dir'] if config.has_option('gap_handler', 'output_dir') else str(
        Path.cwd())
    output_dir_name = output_dir_name.replace('${home}', str(home))
    output_dir: Path = Path(output_dir_name)
    ystart, yend = get_gps_day(offset=-1)
    if ifo is not None:
        def_config = online_dir / f'{ifo.lower()}-channels.ini'
    else:
        def_config = None

    epilog = """
    The default IFO is determined by the domain name of the current host or the environment variable IFO"""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     prog=__process_name__, epilog=epilog)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-i', '--ifo',
                        help='Specify which ifo to search', default=ifo)
    parser.add_argument('-g', '--groups', default='all', nargs='+',
                        help=f'Omicron groups to process, available groups {", ".join(groups)}')
    parser.add_argument('-o', '--output-dir', type=Path, default=str(output_dir),
                        help='Path to directory for condor and command files ')
    parser.add_argument('-f', '--config-file', type=Path, default=def_config,
                        help='Omicron config file')
    parser.add_argument('-l', '--log-file', type=Path,
                        help='Save log messages to this file, default is "omicron-gaps.log" on output-dir')

    parser.add_argument('start', type=to_gps, default=ystart, nargs='?',
                        help='gps time or date/time to start looking for gaps  (yesterday)')
    parser.add_argument('end', type=to_gps, help='end of interval', nargs='?', default=yend)
    parser.add_argument('--condor-accounting-group-user', help='user to use for condor [%(default)s] ',
                        default=acct_user)
    parser.add_argument('-d', '--dry-run', default=False, action='store_true',
                        help='Creates the DAGs but does not submit them')
    parser.add_argument('-n', '--njobs', type=int, default=defnjobs,
                        help='Number of scripts to create, max = 100 [%(default)i]')
    parser.add_argument('--min-gap', type=int, default=defmin,
                        help='Minimum length of a gap to processs [%(default)i]')
    parser.add_argument('--max-gap', type=int, default=defmax,
                        help='Maximumlength of a gap to processs in each DAG [%(default)i]')

    args = parser.parse_args()

    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
        out_verbosity = '--quiet'
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
        out_verbosity = '-v'
    else:
        logger.setLevel(logging.DEBUG)
        out_verbosity = '-vvv'

    output_dir = Path(args.output_dir)
    if args.log_file:
        log_file = Path(args.log_file)
    else:
        log_file = output_dir / "omicron-gap.log"
    output_dir.mkdir(exist_ok=True, parents=True, mode=0o775)

    if not log_file.parent.exists():
        log_file.parent.mkdir(mode=0o775, parents=True)

    log_formatter = logging.Formatter(fmt=log_file_format, datefmt=log_file_date_format)
    log_file_handler = RotatingFileHandler(log_file, maxBytes=10 ** 7, backupCount=5)
    log_file_handler.setFormatter(log_formatter)
    logger.addHandler(log_file_handler)

    logger.debug(f'{myname} running with the following args')
    for arg in vars(args):
        if arg == 'start' or arg == "end":
            alt = f' ({str(from_gps(getattr(args, arg)))})'
        else:
            alt = ''

        logger.debug(f'{arg}: {getattr(args, arg)} {alt}')
    ifo = args.ifo

    if args.config_file:
        config_file = args.config_file
    else:
        config_file = online_dir / f'{ifo.lower()}-channels.ini'

    if not config_file.exists():
        logger.critical(f'Unknown congiguration file for Omicron, {str(config_file)}')

    programs, not_found = which_programs(["python", "omicron-find-gaps", 'conda',
                                          "condor_submit_dag", "omicron-subdag-create"])
    goterr = False

    for prog_name, prog in programs.items():
        if not prog.exists():
            logger.critical(f'Required program {prog.absolute()} does not exist')
            goterr = True
    for prog in not_found:
        logger.critical(f'Required program "{prog}" not found.')
        goterr = True

    goterr &= not check_x509()
    if goterr:
        logger.critical('Please resolve above errors and retry.')
        sys.exit(2)

    proc_groups = args.groups if 'all' not in args.groups else groups
    for group in proc_groups:
        uber_dag = OmicronDag(group)     # dag to process the gap in this group
        uber_dag.logger = logger
        start_str = gps2str(args.start)
        end_str = gps2str(args.end)
        output_grp_dir = output_dir / f'gaps-{group}-{start_str}-{end_str}'
        uber_dag.set_outdir(output_grp_dir)

        # find all gaps we can process in the specified interval
        conda_exe, conda_args = get_conda_run(config, env=conda_env)

        find_args = f'{conda_args} {programs["python"]} '\
                    f'{programs["omicron_find_gaps"]} {out_verbosity} --group {group} --ifo {ifo} ' \
                    f'--config-file {config_file.absolute()} {out_verbosity} ' \
                    f' --output-dir {output_grp_dir} {args.start} {args.end} ' \
                    f' --min-gap {args.min_gap} --max-gap {args.max_gap} '
        find_args += f' --condor-accounting-group-user {args.condor_accounting_group_user}'
        find_job = OmicronTask('FIND', logger, output_grp_dir, group)
        find_job.add_classad('executable', f'{conda_exe}')
        find_job.add_classad('arguments', f'"{find_args}"')
        find_job.add_classad('+InitialRequestMemory', '1024')
        find_job.add_classad('batch_name', 'gap find: $(ClusterID)')
        find_job.add_classad('request_memory', 'ifthenelse(isUndefined(MemoryUsage), 1024, int(3 * MemoryUsage))')
        find_job.update(dict(config['condor']))
        if 'find_fill' in config.sections():
            find_job.update(dict(config['find_fill']))

        uber_dag.add_task(find_job)

        fill_job = OmicronTask('FILL', logger, output_grp_dir, group)
        fill_job.add_classad('executable', '/bin/bash')
        fill_job.add_classad('arguments', '$(script)')
        fill_job.add_classad('+InitialRequestMemory', '1024')
        fill_job.add_classad('batch_name', 'gap fill: $(ClusterID)')
        fill_job.add_classad('request_memory',
                             'ifthenelse(isUndefined(MemoryUsage), 1024, int(3 * MemoryUsage))')

        fill_job.update(dict(config['condor']))
        if 'find_fill' in config.sections():
            fill_job.update(dict(config['find_fill']))
        qglob = output_grp_dir / 'fillgap-*.sh'
        q_cmd = f'script matching {qglob}'
        fill_job.add_classad('queue', q_cmd)

        uber_dag.add_parent_child(find_job.name, fill_job.name)

        uber_dag.add_task(fill_job)

        subdag_path = uber_dag.dagdir / 'omicron_subdag.dag'
        subdag_cr_args = f'-vvv ' \
                         f'--group {group} --inpath {output_grp_dir}  ' \
                         f'--outpath' \
                         f' {subdag_path}'
        create_subdag_script = OmicronScript(is_post=True, parent=fill_job, script=programs["omicron_subdag_create"],
                                             group=group, arguments=subdag_cr_args, name='MAKE_SUBDAG', logger=logger)

        uber_dag.add_task(create_subdag_script)

        subdag_name = 'all_omicron_subdags'
        subdag_job = OmicronSubdag(name=subdag_name, dag_path=subdag_path, logger=logger, group=group)
        uber_dag.add_task(subdag_job)
        uber_dag.add_parent_child(fill_job.name, subdag_job.name)

        uber_dag.write_dag()

        if not args.dry_run:
            cmd = [str(programs['condor_submit_dag'].absolute()), '-import_env', '-force',
                   str(uber_dag.dag_path.absolute())]
            logger.info(f'dag submit: {" ".join(cmd)}')
            res = subprocess.run(cmd, capture_output=True)
            if res.returncode == 0:
                logger.info('dag submit succeeded')
            else:
                err = res.stderr.decode('utf-8')
                logger.error(f'dag submission failed. Return value {res.returncode}\n{err}')

    if log_file:
        logger.info(f'Gap handler log file written to: {log_file.absolute()}')
    elap = time.time() - start_time
    logger.info('run time {:.1f} s'.format(elap))


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
