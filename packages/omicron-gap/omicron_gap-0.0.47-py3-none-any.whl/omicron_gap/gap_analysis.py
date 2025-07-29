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
Detailed look at all current channels in all groups

"""

import time

from omicron import segments

start_time = time.time()

import configparser
from logging.handlers import RotatingFileHandler
from pathlib import Path

from matplotlib import use
import time

import os

import argparse
import logging
from gwpy.time import to_gps, tconvert  # noqa: E402

from gwpy.segments import DataQualityFlag, Segment, SegmentList  # noqa: E402
from .gap_utils import find_frame_gaps, find_trig_seg, get_default_ifo, seglist_print  # noqa: E402
import matplotlib   # noqa: E402
from ._version import __version__

ifo, host = get_default_ifo()
home = os.getenv('HOME')

DEFAULT_SEGMENT_SERVER = os.environ.setdefault('DEFAULT_SEGMENT_SERVER', 'https://segments.ligo.org')
matplotlib.use('agg')
datafind_servers = {'L1': 'LIGO_DATAFIND_SERVER=ldrslave.ligo-la.caltech.edu:443',
                    'H1': 'LIGO_DATAFIND_SERVER=ldrslave.ligo-wa.caltech.edu:443'}

plot: matplotlib.figure = None
axes = None
nribbons = 0


# if launched from a terminal with no display
# Must be done before modules like pyplot are imported
if len(os.getenv('DISPLAY', '')) == 0:
    use('Agg')  # nopep8

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'omicron-gap-analysis'


def main():
    global ifo

    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    now = tconvert()

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-i', '--ifo', help='Specify which ifo to search, [%(default)s]', default=ifo)
    parser.add_argument('-g', '--groups', default='all', nargs='+',
                        help='Omicron groups to process, [%(default)s]')
    parser.add_argument('-f', '--config-file', type=Path, required=True,
                        help='Omicron config file')
    parser.add_argument('--condor-accounting-group-user', help='user to use for condor')
    parser.add_argument('-l', '--log-file', type=Path, help='Save log messages to this file')
    parser.add_argument('start', type=to_gps, default=now - 7 * 86400, nargs='?',
                        help='gps time or date/time to start looking for gaps [%(default)s] (7 days ago)')
    parser.add_argument('end', type=to_gps, help='end of interval [%(default)s] (now)',
                        nargs='?', default=now)
    parser.add_argument('-o', '--output-dir', type=Path, help='Where to store results. Path to directory.')

    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    out_dir: Path = args.output_dir
    out_dir.mkdir(0o775, parents=True, exist_ok=True)
    log_file = Path(args.log_file) if args.log_file else out_dir / 'gap-analysis.log'

    if not log_file.parent.exists():
        log_file.parent.mkdir(mode=0o775, parents=True)
    log_formatter = logging.Formatter(fmt=log_file_format,
                                      datefmt=log_file_date_format)
    log_file_handler = RotatingFileHandler(log_file, maxBytes=10 ** 7,
                                           backupCount=5)
    log_file_handler.setFormatter(log_formatter)
    logger.addHandler(log_file_handler)
    logger.info('Find gaps started')

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    ifo = args.ifo
    start = int(args.start)
    end = int(args.end)

    if ifo is not None:
        default_datafind_server = datafind_servers[ifo]
    else:
        default_datafind_server = os.environ.setdefault('GWDATAFIND_SERVER', 'ldrslave.ligo.caltech.edu:443')

    config = configparser.ConfigParser()
    config_file = Path(args.config_file)
    config.read(config_file)

    groups = config.sections()
    logger.debug(f'There are {len(groups)} groups in config file: {config_file.absolute()}')
    frame_types = dict()
    dq_segments = dict()
    grd_segments = dict()
    grd_seg_def = dict()

    out_dir: Path = args.output_dir
    out_dir.mkdir(0o775, parents=True, exist_ok=True)

    # collect common information from all groups
    for group in groups:
        frame_type = config[group]['frametype']
        frame_types[frame_type] = SegmentList()
        seg_name = config[group]['state-flag'] if 'state-flag' in config[group] else 'None'
        dq_segments[seg_name] = SegmentList()

        try:
            if seg_name == 'None':
                grd_seg_def[seg_name] = None
            else:
                statechannel, statebits, stateft = segments.STATE_CHANNEL[seg_name]
                grd_seg_def[seg_name] = (statechannel, statebits, stateft)
        except KeyError as e:
            logger.critical(f'We do not have a guardian channel corresponding to {seg_name}: {e}')
            grd_seg_def[seg_name] = None

        channels = config[group]['channels'].split('\n')
        logger.info(f'Group: {group}: frame type: {frame_type}, segment: {seg_name}, {len(channels)} channels')

    # anticipate request ending in the future
    now_gps = int(tconvert())
    last_known = SegmentList([Segment(min(now_gps, end), end)])

    # Get frame availability
    for frame_type in frame_types.keys():
        frame_types[frame_type] = find_frame_gaps(ifo, frame_type, start, end, logger, default_datafind_server)

    # Get Segment information
    full_seg = SegmentList([Segment(start, end)]) - last_known

    for seg_name in dq_segments.keys():
        if len(dq_segments[seg_name]) > 0:
            continue
        seg_start = time.time()
        logger.info(f'Get DQ flag {seg_name}, {start}, {end}, url={DEFAULT_SEGMENT_SERVER}')
        if seg_name == 'None':
            dq_segments[seg_name] = DataQualityFlag(name=seg_name, active=full_seg, known=full_seg, label='No seg')
            grd_segments[seg_name] = dq_segments[seg_name]
        else:
            os.unsetenv('HTTPS_PROXY')
            dq_segments[seg_name] = DataQualityFlag.query_dqsegdb(seg_name, start, end, url=DEFAULT_SEGMENT_SERVER)
            elap = time.time() - seg_start
            logger.info(f'Getting segment: {seg_name} took {elap:.1f}s')

            grd_start = time.time()
            statechannel = grd_seg_def[seg_name][0]
            stateft = grd_seg_def[seg_name][2]
            # grd_segments[seg_name] = segments.get_guardian_segments(statechannel, stateft, start, end, pad=(0,0))
            elap = time.time() - grd_start
            logger.info(f'Segments from guardian channel {statechannel} ignored took {elap:.1f}s')

    for frame_type, dqflag in frame_types.items():
        seglist_print(out_dir, dqflag.active, f'frame_{frame_type}_seg')

    for segname, segs in dq_segments.items():
        seglist_print(out_dir, segs.active, f'dqsegment_{segname}_seg')

    # generate plots by group
    for group in groups:
        channels = config[group]['channels'].split('\n')
        seg_name = config[group]['state-flag'] if 'state-flag' in config[group] else 'None'
        frame_type = config[group]['frametype']
        logger.info(f'group: {group}, frame: {frame_type}, dq_seg {seg_name}, channel count: {len(channels)}')

        dq_segs = dq_segments[seg_name]
        frame_segs = frame_types[frame_type]
        want_segs = dq_segs & frame_segs
        seglist_print(out_dir, want_segs.active, f'{group}_want_segs')
        if len(want_segs.active) == 0:
            logger.info(f'group: {group} has no needed times to run.')
            continue
        trig_gaps = dict()
        trig_ok = list()
        trigs_none = list()

        for channel in channels:
            active = find_trig_seg(channel, start, end)
            missing = want_segs.active - active
            if len(active) > 0:
                if len(missing) > 0:
                    known = SegmentList([Segment(start, end)]) - last_known
                    trig_flag = DataQualityFlag(name=channel, known=known, active=active,
                                                label=f'trig({group}): {channel}')

                    trig_gaps[channel] = trig_flag
                    seglist_print(out_dir, trig_flag.active, f'{channel}-trig-availability')
                else:
                    trig_ok.append(channel)
            else:
                trigs_none.append(channel)

        logger.info(f'group: {group}, channels: {len(channels)}, OK: {len(trig_ok)}, '
                    f'missing: {len(trigs_none)}, gaps: {len(trig_gaps)}')
        if len(trigs_none) > 0:
            out_missing = out_dir / f'{group}-missing-channels.txt'
            with out_missing.open('w') as out:
                for channel in trigs_none:
                    print(channel, file=out)
            logger.info(f'group: {group} list of channels with no trigger files written to {out_missing.absolute()}')

        if len(trig_ok) > 0:
            out_ok = out_dir / f'{group}-ok-channels.txt'
            with out_ok.open('w') as out:
                for channel in trig_ok:
                    print(channel, file=out)
            logger.info(f'group: {group} list of channels with expected trigger files written to {out_ok.absolute()}')

        if len(trig_gaps) > 0:
            out_gaps = out_dir / f'{group}-gaps-channel.txt'
            with out_gaps.open('w') as out:
                for channel in trig_gaps.keys():
                    print(channel, file=out)
            logger.info(f'group: {group} list of channels with missing trigger files written to {out_gaps.absolute()}')

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()
