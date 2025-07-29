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
import json
import os
import time

import pytz
from gwpy.time import tconvert

from omicron_gap.gap_utils import get_default_ifo, get_gwf

start_time = time.time()

import argparse
import logging

import configparser

from pathlib import Path
import re
from ._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'omicron-channel-check'


def parser_add_args(parser, ifo=None, config_default=None):
    """
    update the command line arguments
    :param Path|str config_default: default path to the omicron config file
    :param str ifo: default iffo
    :type parser: argparse.ArgumentParser
    :param  parser: the program's parser object
    :return: None but parser is updated
    """
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-i', '--ifo', help='Specify which ifo to search', default=ifo)
    parser.add_argument('-f', '--config-file', type=Path,
                        help='Omicron config file.', default=Path(config_default))
    parser.add_argument('-g', '--gps', help='gps time to look for channels, default = 12 hrs ago')
    parser.add_argument('--json-dir', default='{home}/public_html/omicron/nagios',
                        help='Path to output nagios style output')
    parser.add_argument('-s', '--size', action='store_true', help='Use sample rate to estimate size of needed data')


def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)
    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    ifo, host = get_default_ifo()
    ifo_tmp = '<ifo>' if ifo is None else ifo
    home = os.getenv('HOME')
    config_default = f"{home}/omicron/online/{ifo_tmp.lower()}-channels.ini"
    now = tconvert()

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_add_args(parser, ifo, config_default)

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

    ifo: str = args.ifo
    json_dir = re.sub('{home}', home, args.json_dir)
    json_dir = re.sub('{ifo}', ifo, json_dir)
    json_dir = Path(json_dir)

    if args.config_file:
        config_file = Path(args.config_file)
    else:
        config_file = Path(home) / f'omicron/online/{ifo.lower()}-channels.ini'

    logger.info(f'Config file: {config_file}')
    config = configparser.ConfigParser()
    config_file = Path(config_file)
    config.read(config_file)

    if args.gps:
        gps = int(args.gps)
    else:
        gps = int(now) - 12 * 3600

    logger.info(f'Looking for files at {gps} - {tconvert(gps)}')

    frame_gwf = dict()
    nchannels = 0
    nmissing = 0
    missing_channels = dict()
    groups = config.sections()
    groups.sort()
    total_data_rate = 0
    for group in groups:
        frame_type = config[group]['frametype']
        channels = config[group]['channels'].split('\n')
        nchannels += len(channels)
        logger.info(f'Processing group: {group} with {len(channels)} channels')
        if frame_type not in frame_gwf.keys():
            frame_gwf[frame_type] = get_gwf(ifo, frame_type, gps, gps + 1, logger)
        grp_missing = list()
        grp_data_rate = 0
        for chan in channels:
            if chan not in frame_gwf[frame_type].get_channel_list():
                logger.critical(f'Missing channel {chan} in group: {group}')
                grp_missing.append(chan)
            else:
                chan_data = frame_gwf[frame_type].get_frvect_data(chan)
                grp_data_rate += chan_data["data_rate"]
                total_data_rate += chan_data["data_rate"]
        missing_channels[group] = grp_missing
        misses = len(grp_missing)
        nmissing += misses
        logger.info(f'group: {group}, frame type: {frame_type}, channel count: {len(channels)} '
                    f'missing: {misses} data rate: {grp_data_rate} bytes/second')

    logger.info(f'ifo: {ifo}, groups: {len(config.sections())}, channels: {nchannels}, missing: {nmissing}'
                f'Total input data rate {int(total_data_rate):,d}')
    for group, missing in missing_channels.items():
        nagios_stat = dict()
        nagios_stat['created_gps'] = int(now)
        nagios_stat['created_datetime'] = tconvert(now).astimezone(pytz.UTC).strftime('%c %Z')
        nagios_stat['author'] = dict()
        nagios_stat['author']['name'] = 'Joseph Areeda'
        nagios_stat['author']['email'] = 'joseph.areeds@ligo.org'
        nagios_stat['status_intervals '] = list()
        stats0 = {
            "start_sec": 0,
            "end_sec": 3600 * 36,
            "num_status": 1,
            "txt_status": "No missing channels in omicron configuration"
        }
        stats1 = {
            "start_sec": 3600 * 36,
            "num_status": 3,
            "txt_status": "Omicron channel availability check is not running"
        }
        nchan = len(missing)
        if nchan == 0:
            nagios_stat['status_intervals '].append(stats0)
            nagios_stat['status_intervals '].append(stats1)
        else:
            print(f'{group} has {len(missing)} missing channels')
            stats0['num_status'] = 2
            stats0['txt_status'] = 'Channels in omicron configuration not found in current frames'
            for m in missing:
                print(f'    {m}')
                stats0['txt_status'] += f'\n{m}'
            nagios_stat['status_intervals '].append(stats0)
            nagios_stat['status_intervals '].append(stats1)

        json_file = json_dir / group / f'nagios-chancheck-{group}.json'
        json_file.parent.mkdir(0o775, parents=True, exist_ok=True)
        with json_file.open('w') as jfp:
            json.dump(nagios_stat, jfp, indent=4)

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()
