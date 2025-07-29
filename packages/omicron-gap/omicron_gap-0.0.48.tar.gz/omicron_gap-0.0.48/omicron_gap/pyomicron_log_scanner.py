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
Identify problem runs of pyomicron by examining log files and comparing commands with triggers produced.

1. Find Omicron parameter files. Check gps times against available triggrs.
2. Generate statistics that can be further summarized and plotted with omicron-plot-log-scrapper
"""

import glob
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

from gpstime import tconvert
from gwpy.time import to_gps, from_gps
from omicron.utils import gps_to_hr, deltat_to_hr

from omicron_gap.gap_utils import read_segfile, chans_from_parameters, find_trig_seg, get_default_ifo, get_gps_day, \
    get_default_config, find_segs_to_process, VERBOSE
from omicron_gap.pyomicron_log import PyomicronLog, CondorLog, JobStatistics, JobLog, PyOmicronStatistics, \
    ProcessParameters, ProcParamStatistics

start_time = time.time()

import argparse
import logging
from pathlib import Path
import sys
import traceback

from gwpy.segments import (DataQualityFlag, Segment, SegmentList)

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = Path(__file__).name

logger = None

job_satistics: JobStatistics | None = None
omicron_statistics: PyOmicronStatistics | None = None
proc_param_stats: ProcessParameters | None = None

DEF_SEGMENT = '{ifo}:DMT-GRD_ISC_LOCK_NOMINAL:1'
ifo, host = get_default_ifo()
def_segment = DEF_SEGMENT.format(ifo=ifo)


def no_segs(pyomicron_log, day_seg):
    """
    No analyzable segments noted, verify
    :param PyomicronLog pyomicron_log: log object
    :param SegmentList day_seg: segment_to_process list covering a day
    :return str: new satus
    """
    want_seg = pyomicron_log.segment_to_process
    if want_seg is None:
        status = f'{pyomicron_log.path} has no process segment_to_process'
    else:
        want_seg_len = f'{abs(want_seg)}'
        if day_seg is None:
            dqseg = DataQualityFlag.query_dqsegdb(def_segment, want_seg[0], want_seg[1])
            active_segs = dqseg.active
        else:
            active_segs = day_seg
        non_seg = SegmentList([want_seg])
        for seg in active_segs:
            seg2 = SegmentList([Segment(int(seg[0]), int(seg[1]))])
            non_seg -= seg2
        non_seg_len = abs(non_seg)
        seg_str = f'{gps_to_hr(want_seg[0])} - {gps_to_hr(want_seg[1])}'
        status = (f'Process segment_to_process {seg_str} length: {want_seg_len}, not active: {non_seg_len:.0f} active: '
                  f'{int(want_seg_len) - non_seg_len:.0f} seconds')
    return status


def proc_params(path):
    """
    Find any Omicron parameter files inside path.
    Compare channels and times with triggers published
    :param Path path: path to pyomicron directory
    :return str:  status ok, no analyzable segments, mising triggers
    """
    logger.debug(f'Checking {path.name}')
    seg_file = path / 'segments.txt'
    if not seg_file.is_file():
        return "no segments.txt"

    segs = read_segfile(seg_file)
    start = segs[0][0]
    end = segs[0][1]
    seg_len = abs(segs[0])

    param_files = list(path.glob('parameters/parameters-*.txt'))
    if len(param_files) == 0:
        return 'No parameter files'

    logger.debug(f'Found {len(param_files)} parameter files')
    ermsg = ''
    nchan = 0
    nerchan = 0
    erchans = dict()
    for param in param_files:
        chans = chans_from_parameters(param)
        nchan += len(chans)
        logger.debug(f'Checking {param.name} {len(chans)} channels')

        for cn, chan in enumerate(chans):
            try:
                tsegs = find_trig_seg(chan, start, end)
                if len(tsegs) == 0:
                    nerchan += 1
                    tseg_key = 'None'
                    if tseg_key in erchans.keys():
                        erchans[tseg_key].append(chan)
                    else:
                        erchans[tseg_key] = [chan]
                    ermsg += (f'path: {path.name} chan: {chan}, {start} - {end}, '
                              f'no triggers found, seg len: {seg_len} \n')
                else:
                    tseg_key = str(tsegs)
                    tseg_len = abs(tsegs[0])
                    logger.debug(f'{cn}) Checking {chan} {len(tseg_key)} trigger segments {tseg_key}, \n'
                                 f'     chan trig len: {tseg_len}, seg len: {seg_len} ')
                    if abs(tseg_len - seg_len) > 1:
                        nerchan += 1
                        if tseg_key in erchans.keys():
                            erchans[tseg_key].append(chan)
                        else:
                            erchans[tseg_key] = [chan]
                        ermsg += (f'path: {path.name} chan: {chan}, {start} - {end}, '
                                  f'triggers missing trig len: {tseg_len}, seg len: {seg_len} \n')
            except TypeError as ex:
                p = f'{path.parent.name} / {path.name}'
                logger.error(f'{ex} path: {p} chan: {chan}, {start} - {end}')
                pass
            pass        # good breakpoint location

    omicron_log_path = path / 'logs' / 'omicron.log'
    if omicron_log_path.is_file():
        logger.log(VERBOSE, f'Omicron log found: {omicron_log_path}')
        omicron_log = CondorLog(omicron_log_path, logger)
        omicron_log_summary = omicron_log.summary()
        logger.info(omicron_log_summary)
        if job_satistics is not None:
            job: JobLog
            for job in omicron_log.jobs.values():
                job_satistics.add(job)

    if ermsg == '':
        stat = f'OK. {nchan} channels in {len(param_files)} parameter files have expected trigger file duration'
    else:
        stat = f'{nerchan} channels out of {nchan} are missing triggers\n'
        if logger.level <= logging.DEBUG:
            stat = ermsg

        klist = list(erchans.keys())
        klist.sort()
        stat += '\n'
        for k in klist:
            stat += f'{k}: {len(erchans[k])} channels\n'

    return stat


def parser_get_args():
    """
    Set up command parser and parse the command line
    :return NameSpace: None but parser object is updated
    """
    now = datetime.now()
    this_month = now.strftime("%m")

    epilog = """
    Choose either a specific date, a month, or a list of files, directories or glob patterns, or daily.
    Be sure to quote or escape the wildcard characters, if the resulting list would be too long for the shell.

    The daily analysis puts all results in ${HOME}/public_html/omicron-log-analysis/YYYYMMDD and
    calls omicron-plot-log-scrapper
    """

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__, epilog=epilog,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')

    parser.add_argument('--ifo', default=ifo, type=str, help='IFO if not automatic')
    parser.add_argument('-g', '--group', nargs='*', default='all')

    parser.add_argument('--online-dir', type=Path, default=Path('/home/detchar/omicron/online'),
                        help='Useful debugging on offline systems')
    parser.add_argument('-l', '--logdir', type=Path,
                        default=Path.home() / 'omicron' / 'online' / 'log-scrape', help='Logging directory')
    parser.add_argument('--stat-dir', type=Path, help='Path to statistics output directory')
    parser.add_argument('--tag', type=str, default='', help='Text to add to output files')

    select_group = parser.add_mutually_exclusive_group(required=True)
    select_group.add_argument('-d', '--date', type=to_gps, nargs='*', default=[], help='Date of analysis')
    select_group.add_argument('--month', default=this_month, help='Process specified month (1-12)')
    select_group.add_argument('dirs', nargs='*', help='directory paths or globs to scan')
    select_group.add_argument('--daily', default=False, action='store_true',
                              help='Use defaults for ondor driven daily analysi')

    args = parser.parse_args()
    return args


def proc_dir(indir, group, day_seg, gaps):
    """
    Process a diectory and any subdirectories with Condor logs
    :param Path|str indir: directory to scan
    :param str group: omicron process group if known
    :param SegmentList|None day_seg: segments with expected triggers
    :param SegmentList|None gaps: segments with missing triggers

    :return: None
    """
    dir_start = time.time()
    dlist = glob.glob(str(indir))
    dlist.sort()
    logger.info(f'Scanning {indir} with {len(dlist)} subdirectories')
    dir_segs = SegmentList()
    loglevel = VERBOSE
    for d in dlist:
        pd = Path(d)

        omicron_log_path = pd / 'logs' / 'omicron.log'
        if omicron_log_path.is_file():
            logger.log(VERBOSE, f'Omicron log found: {omicron_log_path}')
            omicron_log = CondorLog(omicron_log_path, logger)
            omicron_log_summary = omicron_log.summary()
            logger.log(VERBOSE, omicron_log_summary)
            if job_satistics is not None:
                job: JobLog
                for job in omicron_log.jobs.values():
                    job_satistics.add(job)

        pyomicron_log_path = pd / 'pyomicron.log'
        if not pyomicron_log_path.exists():
            pyomicron_log_path = pd / 'omicron-process.log'
        if not pyomicron_log_path.exists():
            continue
        pyomicron_log = PyomicronLog(pyomicron_log_path, logger)
        if not pyomicron_log.valid:
            logger.info(f'{pyomicron_log_path} not valid')
            continue

        frame_age = int(pyomicron_log.frame_age)
        if frame_age >= 1200:
            logger.info(f'Frame age: {frame_age}')
        else:
            logger.log(VERBOSE, f'Frame age: {frame_age}')
        if pyomicron_log.segment_to_process is not None:
            dir_segs.append(pyomicron_log.segment_to_process)

        if pyomicron_log.frame_cache is not None and not pyomicron_log.frame_cache.exists():
            logger.info(f'{pyomicron_log.frame_cache.absolute()} does not exist')

        loglevel = VERBOSE
        status = ''
        if 'No parameter files' in status:
            if pyomicron_log.too_short:
                status = f'Processing segment_to_process too short ({abs(pyomicron_log.segment_to_process)}'
                loglevel = VERBOSE
            if pyomicron_log.no_analyzeable:
                status = 'No analyzable segments: ' + no_segs(pyomicron_log, day_seg)
                loglevel = VERBOSE
            if pyomicron_log.stalled:
                status = (f'pyomcron stalled getting state from raw frames:\n'
                          f'       {gps_to_hr(pyomicron_log.segment_to_process[0])} to '
                          f'{gps_to_hr(pyomicron_log.segment_to_process[1])}'
                          f' {abs(pyomicron_log.segment_to_process)} seconds')
                loglevel = logging.INFO
        if gaps.intersects_segment(pyomicron_log.segment_to_process):
            status += f'This process segment_to_process {pyomicron_log.segment_to_process} intercepts gaps'
            loglevel = logging.INFO

        process_parameters = ProcessParameters(pd, logger)
        status = process_parameters.proc_params()
        # loglevel is used to allow normal verbosity (INFO) to only report possible problem directories
        if status.startswith('OK'):
            loglevel = VERBOSE
        else:
            loglevel = logging.INFO

        pyomicron_log.add_params(process_parameters)
        logger.log(loglevel, f'{group} {pd.name} - status: {status}')
        if omicron_statistics is not None:
            omicron_statistics.add(pyomicron_log)
        pass
    if len(dlist) > 0:
        elapsed = time.time() - dir_start
        nsegs = len(dir_segs)
        dir_segs.coalesce()
        nsegs2 = len(dir_segs)
        segs_len = sum(abs(sg) for sg in dir_segs) if dir_segs is not None else 0
        day_seg_len = sum(abs(sg) for sg in day_seg) if day_seg is not None else 0
        missing = day_seg_len - segs_len

        logger.log(loglevel, f'Group {group} dir {indir} in {elapsed:.1f} seconds. \n'
                   f'  {nsegs} segments examined, {nsegs2} colesced covering {deltat_to_hr(segs_len)} '
                   f'day_seg length {deltat_to_hr(day_seg_len)}, missing {deltat_to_hr(missing)}\n'
                   f'  {dir_segs}')


def main():
    global logger, job_satistics, omicron_statistics, proc_param_stats

    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    log_formatter = logging.Formatter(fmt=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__, )
    logger.setLevel(logging.DEBUG)

    args = parser_get_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    elif verbosity < 3:
        logger.setLevel(VERBOSE)
    else:
        logger.setLevel(logging.DEBUG)

    if args.date:
        gps1 = args.date[0]
        dt = from_gps(gps1)
        logfile_name = dt.strftime('%Y%m%d') + '.log'
        args.logdir.mkdir(exist_ok=True, parents=True, mode=0o775)
        logfile = args.logdir / logfile_name
        log_file_handler = RotatingFileHandler(logfile, maxBytes=10 ** 7, backupCount=5)
        log_file_handler.setFormatter(log_formatter)
        logger.addHandler(log_file_handler)
    else:
        logfile = None

    # debugging?
    logger.log(VERBOSE, f'{__process_name__} version: {__version__} running on {host} ')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    ifo = args.ifo
    tag = args.tag
    if tag == '':
        tag = args.group

    if args.stat_dir is not None:
        stat_dir = Path(args.stat_dir)

        stat_base = f'{ifo}-{tag}'
        job_stat_path = stat_dir / f'{stat_base}-job_stats.csv'
        job_satistics = JobStatistics(job_stat_path, logger=logger)
        logger.log(VERBOSE, f'Job statistics: {job_stat_path}')

        omicron_stat_path = stat_dir / f'{stat_base}-omicron_stats.csv'
        omicron_statistics = PyOmicronStatistics(omicron_stat_path, logger=logger)
        logger.log(VERBOSE, f'Omicron statistics: {omicron_stat_path}')

        proc_param_stat_path = stat_dir / f'{stat_base}-proc_param_stats.csv'
        proc_param_stats = ProcParamStatistics(proc_param_stat_path, logger=logger)
        logger.log(VERBOSE, f'Process parameter statistics: {proc_param_stat_path}')

    config = get_default_config(ifo)
    grp_file = args.online_dir / f'{ifo.lower()}-groups.txt'
    all_groups = list()
    with open(grp_file, 'r') as f:
        for line in f:
            line = line.strip()
            all_groups.append(line)

    for online_dir in args.dirs:
        group = '?' if args.group is None else args.group
        group = group.upper()
        for grp in all_groups:
            if grp.lower() in online_dir.lower():
                group = grp
                break
        online_dir = Path(online_dir)
        day_seg = SegmentList([])
        gaps = SegmentList([])

        proc_dir(online_dir, group, day_seg, gaps)

    for ingps in args.date:
        gps_day = get_gps_day(ingps)

        dt = from_gps(ingps)
        mon = dt.strftime('%Y%m')
        day = dt.strftime('%Y%m%d')

        ingrps = all_groups if 'all' in args.group else args.group
        for group in ingrps:
            if 'PEM' in group:
                s = Segment(gps_day)
                now_gps = int(tconvert())
                s_end = min(s[1], now_gps)
                s_day = Segment(s[0], s_end)
                day_seg = SegmentList([s_day])
            else:
                segs = DataQualityFlag.query_dqsegdb(def_segment, gps_day[0], gps_day[1])
                day_seg = segs.active

            gaps = find_segs_to_process(config, ifo, group, gps_day[0], gps_day[1], logger)
            dir_pattern = args.online_dir / group / mon / f'{day}*'
            proc_dir(dir_pattern, group, day_seg, gaps.active)

            pass        # good place for a breakpoint
    if logfile is not None:
        logger.info(f'Logs written to {str(logfile.absolute())}')

    if job_satistics is not None:
        job_satistics.write()
        logger.info(f'Condor job statistics written to {job_satistics.path.absolute()}')

    if omicron_statistics is not None:
        omicron_statistics.write()
        logger.info(f'Omicron statistics written to {omicron_statistics.path.absolute()}')

    if proc_param_stats is not None:
        proc_param_stats.write_output()
        logger.info(f'Process parameter statistics written to {proc_param_stats.path.absolute()}')


if __name__ == "__main__":
    try:

        main()
    except (ValueError, TypeError, OSError, NameError, ArithmeticError, RuntimeError) as ex:
        print(ex, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    if logger is None:
        log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
        log_file_date_format = '%m-%d %H:%M:%S'
        logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
        logger = logging.getLogger(__process_name__)
        logger.setLevel(logging.DEBUG)
    # report our run time
    elap = int(time.time() - start_time)
    logger.info(f'Elapsed time: {deltat_to_hr(elap)}')
