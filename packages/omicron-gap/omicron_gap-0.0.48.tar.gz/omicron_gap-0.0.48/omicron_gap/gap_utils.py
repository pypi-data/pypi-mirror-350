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
"""Set of functions to support finding omicron gaps"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import logging
from configparser import ConfigParser

import os
import re
import shutil
import subprocess
from datetime import timezone, timedelta
from pathlib import Path
import socket

from astropy.time import Time
from astropy.table import vstack as vstack_tables

from gwpy.segments import Segment, SegmentList, DataQualityFlag
from gwpy.table import EventTable
from gwpy.time import tconvert
from gwtrigfind import find_trigger_files
from LDAStools import frameCPP
from gwdatafind import find_urls

from omicron_gap.Gwf import Gwf

DEFAULT_SEGMENT_SERVER = os.environ.setdefault('DEFAULT_SEGMENT_SERVER', 'https://segments.ligo.org')
VERBOSE = 15    # log level between info and debug

gw_data_find = shutil.which('gw_data_find')
fpat = '^(.+)-(\\d+)-(\\d+).(.+)$'
fmatch = re.compile(fpat)


def filename2segment(path):
    """
    generate a segment from a trigger or frame file with a standard name
    :param path:
    :return:
    """
    _, _, a, b = Path(path).name.split('-')
    start = float(a)
    duration = float(b.split('.')[0])
    return Segment(start, start + duration)


def merge_segs(seg_list):
    """
    Merge any contiguous segments in list
    :param SegmentList seg_list: input list
    :return SegmentList: merged list
    """
    ret = SegmentList()
    n = len(seg_list)
    if n > 0:
        cur_seg = Segment(seg_list[0])
        for i in range(1, n):
            nxt_seg = Segment(seg_list[i])
            if cur_seg.end >= nxt_seg.start:
                cur_seg += nxt_seg
            else:
                ret.append(cur_seg)
                cur_seg = nxt_seg
        ret.append(cur_seg)
    return ret


def find_trig_gaps(config, group, start, end):
    """
    Use gwtrigfind to locate any gaps in trigger files regardless of detector state or frame availaability
    :param ConfigParser config: parsed omicron channel list ini file
    :param str group: group name
    :param LIGOTimeGPS start: start of segment to search
    :param LIGOTimeGPS end: end of segment to search
    :return SegmentList: list of segments wth no gaps
    """
    search_interval = SegmentList([Segment(start, end)])
    chans = config[group]['channels']
    chan = chans.splitlines()[0]
    tseg = find_trig_seg(chan, start, end)
    tseg = search_interval - tseg
    return chan, tseg


def find_trig_seg(chan, start, end):
    """
    Return segments when triggers are available
    :param str chan: channel name real
    :param int start: gps time of the start of search
    :param int end: gs time for end of search
    :return SegmentList: SegmentList of times when triggers are availabl
    """
    search_interval = SegmentList([Segment(start, end)])

    try:
        known_files = find_trigger_files(chan, 'omicron', start, end, ext='h5')
        known_files.sort()
        known_segs = SegmentList(map(filename2segment, known_files)) & search_interval
        known_segs = merge_segs(known_segs)
    except ValueError:
        # no directory for this channel/ETG
        known_segs = SegmentList()
    return known_segs


def find_frame_availability(ifo, frame_type, start, end, logger, datafind_server='ldrslave.ligo.caltech.edu:443'):
    """

    :param ifo:
    :param frame_type:
    :param start:
    :param end:
    :param logger:
    :param datafind_server:
    :return:
    """
    gaps = find_frame_gaps(ifo, frame_type, start, end, logger, datafind_server)
    gaps.label = f'frame: {ifo[0]}_{frame_type}'
    return gaps


def find_frame_gaps(ifo, frame_type, start, end, logger, datafind_server=None):
    """
    Use gw_datafind to report any gaps in frame availability
    :param ifo:
    :param frame_type:
    :param start:
    :param end:
    :param logger:
    :return DataQualityFlag:
    """
    known = SegmentList([Segment(start, end)])
    active = SegmentList([Segment(start, end)])
    if datafind_server is None:
        datafind_server = os.getenv('GWDATAFIND_SERVER')
    if datafind_server is None or len(datafind_server) < 2:
        datafind_server = os.getenv('LIGO_DATAFIND_SERVER')

    cmd = [gw_data_find, '-o', ifo[0], '-t', frame_type, '-s', str(int(start)), '-e', str(int(end)),
           '--gaps', '-r', datafind_server]
    logger.debug(f'getting gaps in frame: {frame_type}\n{" ".join(cmd)}')
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode == 1 or res.returncode == 2:
        stderr = res.stderr.decode('utf-8')
        gotgap = False
        frgaps = SegmentList()
        for line in stderr.splitlines(keepends=False):
            if gotgap:
                m = re.match('(\\d+)\\s+(\\d+)', line)
                if m:
                    frgaps.append(Segment(int(m.group(1)), int(m.group(2))))
            elif re.match('.*Missing segments:', line):
                gotgap = True
        active -= frgaps
    elif res.returncode != 0:
        logger.error(f'gw_data_find fail for frame type {frame_type}, return: {res.returncode}')
        active = SegmentList()
    flgname = f'{ifo[0]}_{frame_type}'
    ret = DataQualityFlag(name=flgname, known=known, active=active, label=flgname)
    return ret


def check_certs(logger):
    """
    Verify current Kerberos, x509 and scitokens, warn if not
    I think it/s best to report missing but let the programs fail.
    :param logging.Logger logger:
    :return bool: TRUE if all checks pass
    """
    x509_def = Path.home() / 'active_certificates' / 'x509.pem'
    x509_str = os.getenv('X509_USER_PROXY', x509_def)
    x509 = Path(x509_str)
    if x509.exists():
        os.putenv('X509_USER_PROXY', str(x509.absolute()))
        logger.debug(f'Set environment X509_USER_PROXY={str(x509.absolute())}')
    else:
        logger.error(f'x509 not found at {str(x509.absolute())}')

    eci = shutil.which('ecp-cert-info')
    if eci is None:
        logger.error('Program ecp-cert-info not found')
    else:
        res = subprocess.run([eci], capture_output=True)
        stdout = res.stdout.decode('utf-8')
        stderr = res.stderr.decode('utf-8')
        logger.debug(f'ecp-cert-info returned {res.returncode}\n{stdout}\n{stderr}')


def which_programs(progs):
    """
    Find the external programs needed by these programs
    :param list[str] progs: names of programs to find
    :return (dict, list): paths to programs, NB: keys substitute underscores for any non identifier characters and list
    of any programs not found
    """
    ret = dict()
    not_found = list()

    for prog_name in progs:
        prog_path = shutil.which(prog_name)
        if prog_path is None:
            not_found.append(prog_name)
        else:
            key = re.sub('[^a-zA-Z0-9_.]', '_', prog_name)
            ret[key] = Path(prog_path)
    return ret, not_found


def gps2utc(gps):
    """Convert GPS time to string"""
    gps_time = Time(int(gps), format='gps', scale='utc')
    utc = gps_time.datetime.strftime('%Y-%m-%d %H:%M:%S')
    return utc


def get_gps_day(gps=None, offset=None):
    """
    Return gps times from midnight UTC before arg to after
    :param int offset: number of days from today < 0) past > 0 future
    :param gps: Time in the day of interest, default = today (UTC)
    :return int:  start,end of day
    """
    ingps = gps if gps is not None else int(tconvert())
    ingps += offset * 24 * 3600 if offset is not None else 0
    dt = Time(int(ingps), format='gps', scale='utc').to_datetime(timezone.utc)
    start = int(tconvert(dt.strftime('%Y-%m-%d')))
    end = int(tconvert((dt + timedelta(days=1)).strftime('%Y-%m-%d')))
    return start, end


def gps2dirname(gps):
    """
    use gps time to produce month and day strings
    :param gps: input time
    :return str: YYYYMM, YYYYMMDD
    """
    dt = Time(int(gps), format='gps', scale='utc').to_datetime(timezone.utc)
    day = dt.strftime('%Y%m%d')
    mon = dt.strftime('%Y%m')
    return mon, day


def get_default_ifo():
    # if at a site we have a default ifo
    host = socket.getfqdn()
    if 'ligo-la' in host:
        ifo = 'L1'
    elif 'ligo-wa' in host:
        ifo = 'H1'
    else:
        ifo = os.getenv('IFO')
    if ifo is None:
        ifo = 'UK'
    return ifo, host


def read_trig_file(infile):
    """
    Determine type of file, decode file name, read triggers
    :param str|Path infile: pathlike pointer to trigger file
    :return: EventTable, channel name, start gps, duration
    """
    inpath = Path(infile)
    if inpath.exists():
        m = fmatch.match(str(inpath.name))
        if m:
            name = m.group(1)
            strt = int(m.group(2))
            dur = int(m.group(3))

            if inpath.name.endswith('.h5'):
                table = EventTable.read(inpath, path='/triggers', columns=["time", "frequency", "snr"])
            elif inpath.name.endswith('.xml.gz') or inpath.name.endswith('.xml'):
                try:
                    table = EventTable.read(inpath, tablename='sngl_burst', columns=["peak", "peak_freq", "snr"],
                                            use_numpy_dtypes=True)
                    table.rename_column('peak', 'time')
                    table.rename_column('central_freq', 'frequency')
                except ValueError as ex:
                    print(ex)
                    raise ex
            elif inpath.name.endswith('.root'):
                # reading root files fail if there is a : in the name
                table = EventTable.read(inpath, treename='triggers;1', columns=['time', 'frequency', 'snr'])
            else:
                raise ValueError(f'Trigger type is unknown {inpath.name}')
        else:
            raise ValueError(f'File not in standard format: {inpath.name}')
    else:
        raise FileNotFoundError(f'{inpath.absolute()} not found.')

    return table, name, strt, dur


def read_trig_list(files):
    """
    Construct an EventTable from a list of trigger files
    :param list[Path] files: input files
    :return: EventTable, channel name, start gps, duration
    """
    TABLE_META = ('tablename',)

    new: EventTable | None = None
    chan = None
    start = 1999999999
    end = 0

    for trig_file in files:
        trig_tbl: EventTable
        trig_tbl, rchan, rstart, dur = read_trig_file(trig_file)
        start = min(start, rstart)
        end = max(end, rstart + dur)
        if len(trig_tbl) > 0:
            if new:
                new = vstack_tables([new, trig_tbl])
            else:
                new = trig_tbl
        else:
            pass  # place for a breakpoint
    if new is not None and len(new) > 0:
        new.meta = {k: new.meta[k] for k in TABLE_META if new.meta.get(k)}
    return new, chan, start, end


def get_default_config(ifo):
    """
    Load the omicron confiuration fie for this ifo
    :param str ifo: Which observatory
    :return ConfigParser: configuration object
    """
    config_file = Path(f'{os.getenv("HOME")}/omicron/online/{ifo[0].lower()}1-channels.ini')
    config = ConfigParser()
    config.read(config_file)
    return config


def seglist_print(out_dir, seg_list, name, append=False, write_h5=False):
    """
    Print a SegmentList to a text file for humans and an hdf5 file for machines
    :param bool write_h5: if true write segments go an hdf5 file as well as text
    :param Path out_dir: directory for files
    :param SegmentList seg_list: segments to print
    :param str name: base name for output files [no extension]
    :param bool append: if true append to existing file else replace
    :return: None
    """
    if write_h5:
        out_h5 = out_dir / f'{name}.h5'
        if out_h5.exists():
            os.remove(str(out_h5.absolute()))
        seg_list.write(str(out_h5.absolute()), path='/segments')

    out_txt = out_dir / f'{name}.txt'
    mode = 'a' if append else 'w'
    with out_txt.open(mode) as out:
        for seg in seg_list:
            duration = seg[1] - seg[0]
            print(f'{seg[0]}, {seg[1]}, {tconvert(seg[0])}, {tconvert(seg[1])}, {sec2hrdur(duration)}', file=out)


def seglist2str(seg_list):
    """
    Make a nice human readable segment list
    :param SegmentList seg_list:
    :return str: human readable segment list
    """
    ret = ''
    for seg in seg_list:
        duration = seg[1] - seg[0]
        ret += f'{seg[0]}, {seg[1]}, {tconvert(seg[0])}, {tconvert(seg[1])}, {sec2hrdur(duration)}'
    return ret


def sec2hrdur(dur):
    """
    conver secons to human readable form <days> H:MM:SS
    :param int dur: seconds
    :return str: hr duraation
    """
    td = timedelta(seconds=int(dur))
    return str(td)


def get_gwf(obs, typ, start, end, logger=None):
    """
    Return Gwy object for specified frame
    :param obs:
    :param typ:
    :param start:
    :param end:
    :param logger:
    :return:
    """
    ret = None
    flist = find_urls(obs[0], typ, start, end)
    if len(flist) > 0:
        f = flist[0]
        gwf_path = Path(re.sub(r'file://localhost', '', f))
        ret = Gwf(gwf_path)
    else:
        raise ValueError(f'No frames available for {obs[0]}-{typ}, from {start}, {end}')
    return ret


def get_chan_list(obs, typ, start, end, logger=None):
    """
    get a list of all channels in this frame
    :param obs:
    :param typ:
    :param start:
    :param end:
    :return:
    """
    ret = dict()

    flist = find_urls(obs[0], typ, start, end)
    if len(flist) > 0:
        f = flist[0]
        gwf = re.sub(r'file://localhost', '', f)
        stream = frameCPP.IFrameFStream(str(gwf))
        toc = stream.GetTOC()
        adc_list: list = toc.GetADC()
        for chan in adc_list:
            bps, fs = get_adc_info(stream, chan)
            ret[chan] = (bps, fs)

        proc_list: list = toc.GetProc()
        for chan in proc_list:
            bps, fs = get_proc_info(stream, chan)
            ret[chan] = (bps, fs)

        if logger:
            logger.info(f'We found {len(ret)} in {Path(gwf).name}')
    return ret


def get_frvect_data(frdata):
    """
    get pertinent data for this channel
    :param frdata:  framecpp structured
    :return: byrwa oerample, sample frequency
    """
    for frvect in frdata.data:
        dim = frvect.GetDim(0)
        type = frvect.GetType()
        dx = dim.GetDx()
        bps = type2size[type]
        fs = 1 / dx if dx > 0 else 0
        return bps, fs


def get_adc_info(stream, chan):
    """
    create a dictionary of relevant information for this channel
    :param stream: frameCPP stream
    :param chan: channel name
    :return dict: sample rate(fs), bytes per sample (bps)
    """
    adc_data = stream.ReadFrAdcData(0, chan)
    return get_frvect_data(adc_data)


def get_proc_info(stream, chan):
    prc_data = stream.ReadFrProcData(0, chan)
    return get_frvect_data(prc_data)


type2size = {
    frameCPP.FrVect.FR_VECT_C: 1,
    frameCPP.FrVect.FR_VECT_2S: 2,
    frameCPP.FrVect.FR_VECT_4S: 4,
    frameCPP.FrVect.FR_VECT_8S: 8,
    frameCPP.FrVect.FR_VECT_4R: 4,
    frameCPP.FrVect.FR_VECT_8R: 8,
    frameCPP.FrVect.FR_VECT_8C: 8,
    frameCPP.FrVect.FR_VECT_16C: 16,
    frameCPP.FrVect.FR_VECT_STRING: 16,
    frameCPP.FrVect.FR_VECT_1U: 1,
    frameCPP.FrVect.FR_VECT_2U: 2,
    frameCPP.FrVect.FR_VECT_4U: 4,
    frameCPP.FrVect.FR_VECT_8U: 8,
}


def get_max_cmd_line():
    """
    Query bash for the maximum length of a command line
    :return int: number of bytes tat can be on a bash command line
    """
    gcmd = ['/bin/bash', '-c', "getconf ARG_MAX"]
    ret = 1000000   # safe on my mac and ldas
    try:
        res = subprocess.run(gcmd, encoding='utf-8', capture_output=True)
        res.check_returncode()
        ret = int(res.stdout)
    except subprocess.CalledProcessError:
        pass
    return ret


def read_segfile(path, coltype=int):
    """
    Read a segments.txt file writen by pyomicron
    :param Path | str path: file to read
    :param coltype: data type of segment times
    :return SegmentList: list of segments:
    """

    ret = SegmentList.read(path, gpstype=coltype, format="segwizard",)
    return ret


def chans_from_parameters(param):
    """
    Read an Omicron prameter file return channel list
    :param Path param:  parameter file
    :return list[str]: channel list:
    """
    if not param.exists():
        raise FileNotFoundError(f'Parameter file {param} does not exist')

    # looking for lines like "DATA       CHANNELS         H1:SUS-MC2_M1_DAMP_P_IN1_DQ"
    chpat = re.compile('^DATA\\s+CHANNELS\\s+(\\S+)$')
    ret = list()
    with param.open() as f:
        for line in f:
            line = line.strip()
            m = chpat.match(line)
            if m:
                ret.append(m.group(1))
    return ret


def find_segs_to_process(config, ifo, group, start, end, logger=None):
    """
    Put the logic from find_gaps main into this function for use by other progrrams
    :param ConfigParser|Path|str config: Omiron run  conffiguration for t is ifo
    :param str ifo: which IFO
    :param str group: Group to process (GW, STD1 ...) case insensitice here
    :param LIGOTimeGPS | int start:  gps start of interval to analyze
    :param LIGOTimeGPS|int end:gps end o interval to analyze
    :param logging.Logger logger: optional program logger
    :return SegmentList: list of segments that should have trigger but dont
    """
    if isinstance(config, str) or isinstance(config, Path):
        config_path = Path(config)
        myconfig = ConfigParser()
        myconfig.read(config_path)
    else:
        myconfig = config

    if logger is None:
        logging.basicConfig()
        logger = logging.getLogger('find+segs_to_process')
        logger.setLevel(logging.ERROR)

    group = group.upper()

    chan, gaps = find_trig_gaps(myconfig[group], start, end)

    frames = find_frame_gaps(ifo, myconfig[group]['frametype'], start, end, logger)

    if 'state-flag' in myconfig[group].keys():
        logger.debug(f'Get DQ flag {myconfig[group]["state-flag"]}, {start}, {end}, url={DEFAULT_SEGMENT_SERVER}')
        os.unsetenv('HTTPS_PROXY')
        state = DataQualityFlag.query_dqsegdb(myconfig[group]['state-flag'], start, end, url=DEFAULT_SEGMENT_SERVER)
    else:
        state = frames
        state.name = 'state=all'
        state.label = 'state=all'

    gap_known = SegmentList([Segment(start, end)]) & state.active & frames.active
    gap_active_temp = SegmentList([Segment(start, end)]) & gap_known & gaps
    # weed out gaps that are too short
    min_duration = myconfig.getint(group, 'chunk-duration')
    gap_active = SegmentList()
    for gap in gap_active_temp:
        if abs(gap) >= min_duration:
            gap_active.append(gap)

    return DataQualityFlag(f'{group} gaps', gap_active, gap_known)
