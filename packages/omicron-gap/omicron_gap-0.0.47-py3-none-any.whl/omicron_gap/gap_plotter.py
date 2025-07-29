#!/usr/bin/env python
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2019 Joseph Areeda <joseph.areeda@ligo.org>
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
Plot availability of some representative data used by detchar tasks. We use datafind services for
frame availability, dqsegdb for detector state, and gwtrigfind for omicron triggers when
running at an observatory.
"""
import configparser
import re
import traceback
from logging.handlers import RotatingFileHandler
from pathlib import Path

from ja_webutils.PageItem import PageItemImage, PageItemLink
from matplotlib import use
import time
start_time = time.time()

import os
import sys

# if launched from a terminal with no display
# Must be done before modules like pyplot are imported
if len(os.getenv('DISPLAY', '')) == 0:
    use('Agg')  # nopep8


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'omicron-plot-gaps'

import argparse
import logging
from gwpy.time import to_gps, tconvert, from_gps  # noqa: E402
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

from gwpy.segments import DataQualityFlag, Segment, SegmentList  # noqa: E402
from gwpy.plot.segments import SegmentAxes
from .gap_utils import gps2utc, find_frame_availability, find_trig_seg, \
    get_default_ifo, get_gps_day, gps2dirname  # noqa: E402
import matplotlib   # noqa: E402
from gwpy.plot import Plot
from ja_webutils.Page import Page

global plot, ax, ifo, logger

ifo, host = get_default_ifo()
home = os.getenv('HOME')

std_segments = \
    [
        '{ifo}:DMT-GRD_ISC_LOCK_NOMINAL:1',
        '{ifo}:DMT-DC_READOUT_LOCKED:1',
        '{ifo}:DMT-CALIBRATED:1',
        '{ifo}:DMT-ANALYSIS_READY:1',
        'V1:ITF_NOMINAL_LOCK:1'
    ]
master_seg = '{ifo}:DMT-ANALYSIS_READY:1'
v1_segs = ['V1:ITF_NOMINAL_LOCK:1']

std_frames = \
    {
        '{ifo}_HOFT_C00',
        '{ifo}_HOFT_TEST',
        '{ifo}_DMT_C00',
        '{ifo}_R',
        '{ifo}_M',
        '{ifo}_T',
        'SenseMonitor_Nolines_{ifo}_M',
        'SenseMonitor_CAL_{ifo}_M'
    }
v1_frames = {'HoftOnline'}

DEFAULT_SEGMENT_SERVER = os.environ.setdefault('DEFAULT_SEGMENT_SERVER', 'https://segments.ligo.org')
matplotlib.use('agg')
datafind_servers = {'L1': 'GWDATAFIND_SERVER=datafind2.ligo-la.caltech.edu:443',
                    'H1': 'GWDATAFIND_SERVER=ldrslave.ligo-wa.caltech.edu:443'}
if ifo is not None and ifo != 'UK':
    default_datafind_server = datafind_servers[ifo]
else:
    default_datafind_server = os.environ.setdefault('GWDATAFIND_SERVER', 'ldrslave.ligo.caltech.edu:443')


def init_plot(nframes=None, nsegs=None, nchans=None):
    global plot, ax

    plot = Plot()
    if ifo is None:
        nsubplots = 4
        hratios = [1, 1, 1, 1]
    else:
        nsubplots = 3
        if nframes is None:
            hratios = [1.5, 1, 3]
        else:
            hratios = [nframes, nsegs, nchans]

    ax = plot.subplots(nsubplots, 1, sharex='col', subplot_kw={"axes_class": SegmentAxes},
                       gridspec_kw={'height_ratios': hratios[0:nsubplots]})


def monthly_update_start(gps, stride):
    """
    Convert GPS to start of month, with or without adding stride
    :param int gps: GPS time
    :param int stride: number of months to add, use 0 to get gps of first of month
    :return int: gps time of specified first of the month
    """
    in_dt = from_gps(gps)
    gps_mon = in_dt.month + stride
    gps_yr = in_dt.year

    if gps_mon > 12:
        gps_yr += int(gps_mon / 12)
        gps_mon %= 12

    ret = tconvert(f'{gps_mon}/1/{gps_yr}')
    return ret


def plot_seg(seg_data, axnum):
    """
    Add a ribbon for a DataQualityFlag
    :param int axnum: which axis ( we may hve frame, segs, triggers)
    :param DataQualityFlag seg_data:
    :return:
    """

    if plot is None:
        init_plot()

    ax[axnum].plot(seg_data)


def seg_dump(txt, segs, label):
    """
    Write segments to text file
    :param txt: file pointer to file open for writing
    :param dict segs: containing segment lists
    :param str label:
    :return:
    """
    print(f'{label} segments\n=================', file=txt)
    for seg_name, seg_data in segs.items():
        print(f'    {seg_name}:', file=txt)
        active_total = 0
        for seg in seg_data.active:
            seg_dur = seg.end - seg.start
            active_total = active_total + int(seg_dur)
            seg_dur_hr = int(seg_dur) / 3600.
            print(f'  {int(seg.start)} {int(seg.end)}    # ({int(seg_dur)} sec, {seg_dur_hr:.1f} hrs) '
                  f'{gps2utc(seg.start)} {gps2utc(seg.end)}', file=txt)
        print(f'---Total active time for {seg_name} {active_total} seconds, {active_total / 3600.:.1f} hrs\n',
              file=txt)


def parser_add_args(parser):
    """
    Set up command parser
    :param argparse.ArgumentParser parser:
    :return: None but parser object is updated
    """
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    parser.add_argument('start', type=to_gps, action='store', nargs='?', help='Start of plot')
    parser.add_argument('end', type=to_gps, action='store', nargs='?', help='End of plot, default start + 24 hrs')
    parser.add_argument('--yesterday', action='store_true', help='set times to 24 hours covering yesterday')
    parser.add_argument('-E', '--epoch', type=float, action='store',
                        help='Delta < 10000000 or GPS', required=False)
    parser.add_argument('-i', '--ifo', type=str, default=ifo,
                        help='IFO (L1, H1, V1)')
    parser.add_argument('-l', '--log-file', type=Path, help='Save log messages to this file')
    parser.add_argument('-o', '--out', help='Base path to results: txt and png files. Default is '
                                            'a directory in ~/public_html/detchar-avail based on month and day')
    parser.add_argument('-t', '--text', action='store_true', help='Save a text file of all data plotted')
    parser.add_argument('--html', action='store_true', help='Create an overview html file. implies --text')

    parser.add_argument('--std', action='store_true', help='Add "standard" segment list')
    parser.add_argument('-S', '--segments', type=str, nargs='*', default=std_segments,
                        help='List of segments to examine with "{ifo}" ')
    parser.add_argument('-g', '--geometry', help='Width x Height')
    parser.add_argument('-c', '--config', type=Path, help='omicron config default is to look in ~/omicron/online')
    parser.add_argument('--stride', help='Divide time into multiple images. Format: <n><period> where period '
                                         'starts with h[our], d[ay], w[eek], m[onth]')
    parser.add_argument('--chans', nargs='*', help='one or more channel names. Partial case insensitive matching is '
                                                   'done')


def get_proc_chan_list(args, config, logger):
    """
    Set up a list of dictionaries defining which channel triggers to plot
    :param Namespace args:
    :param ConfigParser config:
    :param logger:
    :return list[dict]: channels
    """
    ret = list()

    groups = config.sections()
    groups.sort()

    for trig_group in groups:
        allchans = config[trig_group]['channels'].split('\n')
        frame_type = config[trig_group]['frametype']
        if 'state-flag' in config[trig_group]:
            seg_name = config[trig_group]['state-flag']
        else:
            seg_name = None
        if args.chans:

            for chan_pat in args.chans:
                logger.debug(f'Searching for {chan_pat}')
                for chan_name in allchans:
                    if re.match(f'.*{chan_pat}.*', chan_name, re.IGNORECASE):
                        trig_chan = chan_name
                        chan_def = {'trig_chan': trig_chan, 'frame_type': frame_type, 'seg_name': seg_name,
                                    'trig_group': trig_group, 'nchan_grp': len(allchans)}
                        ret.append(chan_def)
                        break
        else:
            trig_chan = allchans[0]
            chan_def = {'trig_chan': trig_chan, 'frame_type': frame_type, 'seg_name': seg_name,
                        'trig_group': trig_group, 'nchan_grp': len(allchans)}
            ret.append(chan_def)

    return ret


def main():
    global plot, ifo, logger

    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    start_time = time.time()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     prog=__process_name__)
    parser_add_args(parser)
    args = parser.parse_args()

    verbosity = args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    if args.log_file:
        log_file = Path(args.log_file)
        if not log_file.parent.exists():
            log_file.parent.mkdir(mode=0o775, parents=True)
        log_formatter = logging.Formatter(fmt=log_file_format,
                                          datefmt=log_file_date_format)
        log_file_handler = RotatingFileHandler(args.log_file, maxBytes=10 ** 7,
                                               backupCount=5)
        log_file_handler.setFormatter(log_formatter)
        logger.addHandler(log_file_handler)
        logger.info('Find gaps started')

    # debugging?
    logger.debug('{} called with arguments:'.format(__process_name__))
    for k, v in args.__dict__.items():
        if k == 'start' or k == 'end':
            tcon = 'None' if v is None else str(tconvert(v))
            auxinfo = ' - (' + tcon + ' )'
        else:
            auxinfo = ''
        logger.debug(f'    {k} = {v}{auxinfo}')

    ifo = args.ifo
    datafind_server = os.getenv('GWDATAFIND_SERVER')
    datafind_server = default_datafind_server if datafind_server is None else datafind_server
    now_gps = int(tconvert())
    if args.start:
        start = int(args.start)
        if args.end:
            end = int(args.end)
        else:
            end = start + 24 * 3600
    elif args.yesterday:
        start, end = get_gps_day(offset=-1)
    else:
        start, end = get_gps_day()

    period = None
    if args.stride:
        m = re.match('^(\\d+)([hdwmHDWM]\\w*)', args.stride)
        if m:
            stride = int(m.group(1))
            period = m.group(2)[0]
            period = period.lower()

            if period == 'h':
                stride *= 3600
            elif period == 'd':
                stride *= 86400
            elif period == 'w':
                stride *= 86400 * 7
            elif period != 'm':
                raise ValueError(f'Unknown units for stride [{m.group(2)}]')
        else:
            raise ValueError(f'Invalid stride [{args.stride}]')
    else:
        stride = end - start

    last_known = SegmentList([Segment(min(now_gps, end), end)])

    segments = list()
    if args.std or not args.segments:
        segments.extend(std_segments)

    if args.segments:
        segments.extend(args.segments)

    config = None
    conf_file = None
    if args.config:
        conf_file = Path(args.config)
    elif ifo is not None:
        conf_file = Path(f'{home}') / 'omicron' / 'online' / f'{ifo.lower()}-channels.ini'
    if conf_file is None or not conf_file.exists():
        logger.critical('Could not find the config file ')
        # exit(5)
    else:
        logger.info(f'Config file: {str(conf_file.absolute())}')
        config = configparser.ConfigParser()
        config.read(conf_file)

    frame_types = dict()

    # space command line frame types
    ifos = [ifo] if ifo is not None else ['L1', 'H1', 'V1']

    for f in std_frames:
        for i in ifos:
            if i == 'V1':
                frame_types[i] = v1_frames
            else:
                frame_type = f.replace('{ifo}', i)
                if i not in frame_types.keys():
                    frame_types[i] = list()
                frame_types[i].append(frame_type)

    cur_start = start

    if period == 'm':
        # when striding by months we always start on the first
        cur_start = monthly_update_start(cur_start, 0)  # converts to first of month

    nsections = len(list(config.sections()))
    nsegs = len(segments)
    nframes = len(frame_types[ifos[0]])

    while cur_start < end:
        page = Page()
        init_plot(nframes, nsegs, nsections)
        mon, day = gps2dirname(cur_start)
        if period == 'm':
            cur_end = monthly_update_start(cur_start, 1)
        else:
            cur_end = cur_start + stride

        if args.out:
            plot_file = Path(args.out)
            if not plot_file.exists() and args.stride:
                plot_file.mkdir(mode=0o775, parents=True, exist_ok=True)

            if plot_file.is_dir():
                plot_file /= day
        else:
            plot_file = Path.home() / 'public_html' / 'detchar-avail' / mon / day
        plot_file.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
        ext = plot_file.suffix
        if ext:
            plot_base = str(plot_file)[0:-len(ext)]
        else:
            plot_base = str(plot_file)
        plot_file = Path(plot_base + '.png')
        txt_file = Path(plot_base + '.txt')
        html_file = Path(plot_base + '.html')

        frame_segs = dict()
        axnum = -1
        for this_ifo, frset in frame_types.items():
            if frset is not None:
                axnum += 1
                frlist = list(frset)
                frlist.sort()
                for fram in frlist:
                    fr_avail = find_frame_availability(this_ifo, fram, cur_start, cur_end, logger, datafind_server)
                    fr_avail.known -= last_known
                    frame_segs[fram] = fr_avail
                    plot_seg(fr_avail, axnum)

        trigger_segs = dict()

        dq_segs = dict()
        for i in ifos:
            dq_segs[i] = set()
            for segment in segments:
                seg_name = segment.replace('{ifo}', i)
                dq_segs[i].add(seg_name)

            logger.info(f'{len(dq_segs[i])} segs: {", ".join(dq_segs[i])}')
        logger.info(f'from {cur_start} ({tconvert(cur_start)}, to {cur_end} ({tconvert(cur_end)}')
        dqsegs = dict()

        for i in ifos:
            axnum += 1
            for seg_name in sorted(dq_segs[i]):
                try:
                    qstrt = time.time()
                    seg_data = DataQualityFlag. \
                        query_dqsegdb(seg_name, cur_start, cur_end,
                                      url='https://segments.ligo.org')
                    logger.info(f'Segment query for {seg_name} {len(seg_data.known)} known {len(seg_data.active)} '
                                f'active. Query took {int(time.time() - qstrt)} seconds')
                except ValueError:
                    qstrt = time.time()
                    seg_data = DataQualityFlag. \
                        query_dqsegdb(seg_name, cur_start, cur_end,
                                      url='https://segments-backup.ligo.org/')
                    logger.info(f'Backup query for {seg_name} took {int(time.time() - qstrt)} seconds')

                if len(seg_data.known) > 0:
                    if not seg_data.isgood:
                        seg_data = ~seg_data
                    seg_data.label = f'DQ seg: {seg_name}'
                    dqsegs[seg_name] = seg_data
                    plot_seg(seg_data, axnum)

        if ifo is not None and config is not None:
            chan_list = get_proc_chan_list(args, config, logger)
            axnum += 1
            for chan in chan_list:
                trig_chan = chan['trig_chan']
                seg_name = chan['seg_name']
                frame_type = chan['frame_type']
                trig_group = chan['trig_group']
                nchan_grp = chan['nchan_grp']

                active = find_trig_seg(trig_chan, cur_start, cur_end)
                if seg_name is not None:
                    known = dqsegs[seg_name].active & frame_segs[frame_type].active
                else:
                    known = (SegmentList([Segment(cur_start, cur_end)]) - last_known) & frame_segs[frame_type].active
                trig_label = f'trig({trig_group}): {trig_chan} ({nchan_grp})'
                if len(known) == 0:
                    # we need something to plot
                    known = SegmentList([Segment(cur_start, cur_start + 1)])
                trig_flag = DataQualityFlag(name=trig_chan, known=known, active=active,
                                            label=trig_label)
                plot_seg(trig_flag, 2)
                trigger_segs[trig_label] = trig_flag

        axis_titles = list()
        for i in ifos:
            axis_titles.append(f'{i}: Frame availability. Green -> datafind succeeded, Red -> frame not found')
        for i in ifos:
            axis_titles.append(f'{i}: DQ segments. Green -> active segments, red -> known but not active, '
                               'white -> no segments available')
        for i in ifos:
            axis_titles.append(f'{i}: Omicron triggers. Green -> triggers available, red -> missing triggers, '
                               f'white -> no triggers expected')

        if plot is not None:
            n = 0
            for axis in ax:
                axis.xaxis.grid(True, color='b', linestyle='-', linewidth=0.8)
                axis.set_xlim(cur_start, cur_end)
                axis.set_title(axis_titles[n])
                n = n + 1

                epoch = cur_start
                if args.epoch:
                    if args.epoch <= 10000000:
                        epoch += args.epoch
                    else:
                        epoch = args.epoch
                axis.set_epoch(epoch)
            strt_str = tconvert(cur_start).strftime('%Y-%m-%d %H:%M')
            end_str = tconvert(cur_end).strftime('%Y-%m-%d %H:%M')
            now_str = tconvert(now_gps).strftime('%Y-%m-%d %H:%M')
            loc = 'CIT' if ifo is None else 'LLO' if ifo == 'L1' else 'LHO'
            plot.suptitle(f'Detchar data availability at {loc}. {strt_str} to {end_str} created at {now_str}',
                          fontsize=18)

            nribbons = nsections + nsegs + nframes + 1
            height = nribbons * 0.5 + 1.20
            minhgt = 8.0
            logger.info(f'nribbons: {nribbons}, calculated height: {height:.2f}, min: {minhgt:.2f}')
            height = max(height, minhgt)

            plot.set_figwidth(18)
            plot.set_figheight(height)
            plot.savefig(plot_file, edgecolor='white', bbox_inches='tight')
            logger.info(f'Wrote plot to {plot_file}')
        else:
            logger.critical('None of the segment(s) were known during the requested times')
            sys.exit(2)

        if args.text or args.html:
            with txt_file.open('w') as txt:
                seg_dump(txt, dqsegs, 'Data Quality')
                print('', file=txt)
                seg_dump(txt, frame_segs, 'Frame')
                print('', file=txt)
                seg_dump(txt, trigger_segs, 'Omicron triggers')
                print('', file=txt)

            logger.info(f'Text summary of segments written to {str(txt_file.absolute())}')
        if period == 'm':
            cur_start = cur_end
            cur_end = monthly_update_start(cur_start, 1)
        else:
            cur_start = cur_end
            cur_end = cur_start + stride

        plot = None
        if args.html:
            img = PageItemImage(url=plot_file.name, alt_text='availablity plot')
            page.add(img)
            txt_itm = PageItemLink(url=txt_file.name, contents='Text of all specific segments')
            page.add_blanks(2)
            page.add(txt_itm)
            with html_file.open('w') as htfp:
                htfp.write(page.get_html())
            logger.info(f'HTML written to {html_file.absolute()}')
    logger.info('Runtime: {:.1f} seconds'.format(time.time() - start_time))


if __name__ == "__main__":
    global logger
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
