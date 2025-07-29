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
Class  to read pyomcron.log file
"""
import csv
from datetime import datetime
from logging import Logger
from pathlib import Path
import logging

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import re
import sys

import htcondor
from gwpy.segments import Segment, SegmentList
from htcondor import JobEventType
from htcondor2 import JobEvent

from omicron_gap.gap_utils import read_segfile, chans_from_parameters, find_trig_seg, VERBOSE

# Last available frame data: 1413047230 (10/15/24 17:06:52) age: 204 -   00:03:24
frpat = re.compile('^.*Last available frame data: (\\d+).*age:\\s+(\\d+)')

# 'Processing segment_to_process determined as: 1413045428 (10/15/24 16:36:50) - 1413047232 (10/15/24 17:06:54)'
proc_seg = re.compile('^.*Processing segment determined as:\\s+(\\d+).*- (\\d+)')

# No analysable segments found, but up-to-date data are available.
no_segs = 'No analysable segments found, but up-to-date data are available.'


class JobLog:
    """
    Represents a logged job as defined by cluster ID
    """
    def __init__(self, path, event, logger=None):
        """
        :param Path|str: path condor log file
        :param JobEvent event: first event seen with this cluster id
        :param logging.Logger logger: use caller's or create error only
        """
        self.path = path
        self.terminate = None
        self.terminated_normally = None
        self.execute = None
        self.execute_host = ''
        self.execute_history = list()
        self.submit = None
        self.submit_host = ''
        self.log_notes = ''
        self.submit_history = list()
        self.cluster = event.cluster
        self.logger = logger
        self.memory_usage = list()
        self.exit_code = None
        self.exit_who = None
        self.exit_by_signal = False
        self.aborted = None
        self.memory = None
        self.sent_bytes = None
        self.received_bytes = None
        self.evicted = list()

        self.disconnected = list()
        self.reconnect_failed = list()
        self.reconnected = list()

        self.run_local_usage = None

        if self.logger is None:
            self.logger = logging.getLogger('JobLog')
            self.logger.setLevel(logging.ERROR)

        self.update(event)
        pass

    def update(self, event):
        """
        Updateobject  with what we want to keep

        :param JobEvent event:
        :return: None
        """
        if event.cluster != self.cluster:
            self.cluster = event.cluster
            self.logger.debug(f'New cluster: {event.cluster} added to {event.cluster}')

        if event.type == JobEventType.SUBMIT:
            if self.submit is None:
                self.submit = event.timestamp
                self.submit_host = event.get('SubmitHost')
                self.log_notes = event.get('LogNotes')

            submit_dict = {'time': event.timestamp, 'host': self.submit_host, 'notes': self.log_notes}
            self.execute_history.append(submit_dict)
        elif event.type == JobEventType.EXECUTE:
            if self.execute is None:
                self.execute = event.timestamp
                self.execute_host = event.get('ExecuteHost')
            exe_dict = {'time': event.timestamp, 'host': self.execute_host}
            self.execute_history.append(exe_dict)
        elif event.type == JobEventType.IMAGE_SIZE:
            self.memory_usage.append((event.get('MemoryUsage'), event.timestamp))
        elif event.type == JobEventType.JOB_TERMINATED:
            self.terminate = event.timestamp
            toe = event.get('ToE')
            if toe is not None:
                try:
                    self.exit_by_signal = toe['ExitBySignal']
                    self.exit_code = toe['ExitCode']
                    self.exit_who = toe['Who']
                    self.memory_usage.append((event.get('Memory'), event.timestamp))
                    self.memory = event.get('Memory')
                    self.sent_bytes = event.get('SentBytes')
                    self.received_bytes = event.get('ReceivedBytes')
                except KeyError:
                    pass
            else:
                self.exit_code = event.get('ReturnValue')
                self.terminated_normally = event.get('TerminatedNormally')
                self.received_bytes = event.get('TotalReceivedBytes')
                self.sent_bytes = event.get('TotalSentBytes')
                self.run_local_usage = event.get('RunLocalUsage')
            self.logger.debug(f'Job terminated event data has {len(list(event.keys()))} keys')
            spaces = ' ' * 4
            for k, v in event.items():
                self.logger.debug(f'{spaces}Key {k}: {v}')
        elif event.type == JobEventType.JOB_ABORTED:
            self.aborted = event.get('Reason')
        elif event.type == JobEventType.JOB_EVICTED:
            self.evicted.append(event.timestamp)
        elif event.type == JobEventType.JOB_DISCONNECTED:
            self.disconnected.append(event.timestamp)
        elif event.type == JobEventType.JOB_RECONNECT_FAILED:
            self.reconnect_failed.append(event.timestamp)
        elif event.type == JobEventType.JOB_RECONNECTED:
            self.reconnected.append(event.timestamp)
        else:
            self.logger.error(f'Unexpected job event type: {event.type.name}')

    def summary(self, indent=3):
        """
        Prodce a summary of the job
        :param int indent: indent all lines, for inclusion in another report
        :return str: summary of what we know about the job
        """
        ret = ''
        spaces = ' ' * indent
        if self.log_notes is not None:
            ret += f'{spaces}Log notes:{self.log_notes}\n'
        if self.exit_code is not None:
            ret += f'{spaces}ExitCode: {self.exit_code}'
            if self.terminated_normally is not None:
                ret += f' TerminatedNormally: {self.terminated_normally}\n'
        if self.exit_by_signal:
            ret += f'{spaces}ExitBySignal: {self.exit_by_signal}'
        if self.submit is not None and self.execute is not None:
            ret += f'{spaces}Submit to execute: {self.execute - self.submit} seconds\n'
        if self.terminate is not None and self.execute is not None:
            ret += f'{spaces}Execution time: {self.terminate - self.execute} seconds\n'
        if self.memory is not None:
            ret += f'{spaces}Memory usage: {self.memory} MB\n'
        if self.memory_usage is not None:
            ret += f'{spaces}Memory usage: {self.memory_usage} MB\n'
        if self.run_local_usage is not None:
            ret += f'{spaces}Run local usage: {self.run_local_usage}\n'
        return ret

    @staticmethod
    def get_col_labels():
        """
        return list of labels for status information
        :return list[str]: the labels
        """
        return ['Path', 'Name', 'Submitted', 'ClusterID', 'Q-time', 'Run-time', 'Exit-code', 'Memory', 'Local',
                'Signal', 'Aborted',
                'Disconnected count', 'Evicted count', 'Reconnected count', 'Reconnect_failed', 'Terminated normally',]

    def get_stats(self):
        """
        Summarize the job statistics
        :return list[str]: the statistics
        """
        ret = [str(self.path.absolute())]
        name = self.log_notes
        name = name.replace('DAG Node:', '')
        ret.append(name)
        if self.submit is None:
            sub_time = 'NAN'
        else:
            submit_dt = datetime.fromtimestamp(self.submit)
            sub_time = submit_dt.strftime('%Y-%m-%d %H:%M:%S')
        ret.append(sub_time)
        ret.append(self.cluster)
        if isinstance(self.execute, (int, float)) and isinstance(self.submit, (int, float)):
            qtime = f"{self.execute - self.submit:.1f}"
        else:
            qtime = 'nan'
        ret.append(qtime)
        if self.terminate is not None and self.execute is not None:
            etime = f"{self.terminate - self.execute:.0f}"
        else:
            etime = 0
        ret.append(etime)
        ret.append(self.exit_code)
        ret.append(f'{self.memory}')
        local_job = 1 if self.run_local_usage is not None else 0
        ret.append(f'{local_job}')
        exit_by_signal = 1 if self.exit_by_signal else 0
        ret.append(f'{exit_by_signal}')
        aborted = 1 if self.aborted else 0
        ret.append(f"{aborted}")
        ret.append(f'{len(self.disconnected)}')
        ret.append(f'{len(self.evicted)}')
        ret.append(f'{len(self.reconnected)}')
        ret.append(f'{len(self.reconnect_failed)}')
        terminated_normally = 1 if self.terminated_normally is not None else 0
        ret.append(f'{terminated_normally}')

        return ret


class CondorLog:
    jobs: dict[int, JobLog]
    logger: Logger | None

    def __init__(self, path=None, logger=None):
        """
        Specify file to read
        :param Path|str path: file to read
        :param logging.Logger logger: logger to use
        """
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.jobs = dict()

        if self.logger is None:
            self.logger = logging.getLogger('CondorLog')
            self.logger.setLevel(logging.ERROR)

        self.logger.debug(f'Digesting condor log file: {self.path}')
        if self.path is not None:
            if not self.path.exists():
                raise FileNotFoundError(f'Condor log file: {self.path} does not exist')
            self.read(self.path)

    def read(self, path):
        """

        :param Path path:
        :return:
        """

        jel = htcondor.JobEventLog(str(path))
        event: JobEvent
        for event in jel.events(stop_after=0):
            cluster = event.cluster
            if cluster in self.jobs:
                self.jobs[cluster].update(event)
            else:
                self.logger.debug(f'New cluster job: {cluster}')
                self.jobs[cluster] = JobLog(path, event, logger=self.logger)
        pass

    def summary(self):
        """
        Format what we know
        :return str: formatted summary
        """
        ret = f'Summary of {self.path} with {len(self.jobs)} jobs\n'
        if self.has_error():
            ret += f'One or more jobs had non-zero return or killed by signal {self.path}\n'

        for job in self.jobs.values():
            ret += job.summary() + '\n'

        return ret

    def has_error(self):
        """
        Check if any jobs have a non-zero exit code
        :return bool: True if non-zero return code found
        """
        ret = False
        for job in self.jobs.values():
            ret |= job.exit_code != 0 or job.exit_by_signal
        return ret


class JobStatistics:
    """
    Create and try to be efficient writing stats on the job
    """
    def __init__(self, path=None, logger=None):
        """

        :param Path|str path: output csv file
        :param logger logger: logger to use
        """
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.jobs = list()

        if self.logger is None:
            self.logger = logging.getLogger('CondorLog')
            self.logger.setLevel(logging.ERROR)

    def add(self, job: JobLog):
        """
        Extrct what we need from the job
        :param JobLog job:
        :return None:
        """
        self.jobs.append(job)

    def write(self):
        """
        Write the file
        :return:
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w') as f:
            writer = csv.writer(f)
            labels = JobLog.get_col_labels()
            writer.writerow(labels)

            for job in self.jobs:
                stats = job.get_stats()
                writer.writerow(stats)


class PyomicronLog:
    logger: Logger | None
    path: Path | None
    frame_cache: Path | None

    def __init__(self, path=None, logger=None):
        """
        Specify file to read
        :param Path|str path: file to read
        :param logging.Logger logger: logger to use
        """
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.stalled = False
        self.process_params = list()

        if self.logger is None:
            self.logger = logging.getLogger('PyomicronLog')
            self.logger.setLevel(logging.ERROR)

        self.start = None
        self.last_frame = None
        self.frame_age = 0
        self.segment_to_process = None
        self.segment_txt = None
        self.no_analyzeable = False
        self.online = False
        self.frame_cache = None
        self.too_short = False
        self.valid = False
        if self.path is not None:
            self.read(self.path)

    def read(self, path):
        """
        Read pyomcron.log
        :param Path|str path: file to read
        :return: None but object is populated
        """
        logpath = Path(path)
        nlines = logpath.read_text().count('\n')
        if logpath.is_file() and nlines > 5:
            with logpath.open('r') as f:
                for line in f:
                    line = line.strip()
                    if "Online process." in line:
                        self.online = True
                        file_str = logpath.parent.name
                        self.logger.log(15, f'Online process: {file_str}')
                    m = frpat.match(line)
                    if m is not None:
                        self.last_frame = int(m.group(1)) + int(m.group(2))
                        self.frame_age = int(m.group(2))
                        continue
                    m = proc_seg.match(line)
                    if m is not None:
                        self.segment_to_process = Segment(int(m.group(1)), int(m.group(2)))
                        continue
                    if no_segs in line:
                        self.no_analyzeable = True
                        continue
                    if 'The final segment_to_process is too short,' in line:
                        self.too_short = True
                        continue
                    if '/cache/frames.lcf' in line:
                        self.frame_cache = Path(line)
                        if not self.frame_cache.exists():
                            alt_lcf_path = path.parent / 'logs'
                            alt_lcf = list(alt_lcf_path.glob('frames.*.lcf'))
                            if len(alt_lcf) > 0:
                                self.logger.debug(f'Found frame cache in alternate location: {alt_lcf}')
                                self.frame_cache = alt_lcf[0]
                            else:
                                # another place if we've copied the whole directory
                                alt_lcf_path = self.path.parent / 'cache' / 'frames.lcf'
                                if alt_lcf_path.exists():
                                    self.frame_cache = alt_lcf_path
                                else:
                                    self.logger.debug(f'self.frame_cache not found: {self.frame_cache}')
                        continue
                    # if last line matches we stalled
                    self.stalled = 'Finding segments for relevant state...' in line
                self.valid = True
        else:
            self.valid = False

    def add_params(self, process_params):
        self.process_params.append(process_params)

    @staticmethod
    def get_labels():
        """
        return names of columns get_stats produces
        :return list[str]: names of columns get_stats produces
        """
        cols = ['Path', 'FrameAge', 'Wanted segment start', 'end', 'want seg len', 'available trigger len', 'Missing',
                'Too short', 'Stalled', 'Valid', 'No analyzable', 'N-omicron jobs',
                ]
        return cols

    def get_stats(self):
        pseg_len = abs(self.segment_to_process) if self.segment_to_process is not None else 0
        tseg_len = 0
        process_param: ProcessParameters
        for process_param in self.process_params:
            tseg_len += process_param.available_trig_len

        too_short = 1 if self.too_short else 0
        stalled = 1 if self.stalled else 0
        valid = 1 if self.valid else 0
        no_analyzeable = 1 if self.no_analyzeable else 0
        ret = [self.path, self.frame_age, f'{self.segment_to_process[0]:d}', f'{self.segment_to_process[1]:d}',
               pseg_len, tseg_len, (pseg_len - tseg_len), too_short, stalled, valid,
               no_analyzeable, len(self.process_params),
               ]
        return ret


class PyOmicronStatistics:
    """
    Represents what we want to save from pyomicron logs
    """
    def __init__(self, path=None, logger=None):

        """

        :param Path|str path: output csv file
        :param logger logger: logger to use.
        """
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.logs = list()
        self.sizes = 0

    def add(self, log: PyomicronLog):
        """

        :param log:
        :return:
        """
        self.logs.append(log)
        self.sizes += sys.getsizeof(log)
        pass

    def write(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w') as f:
            writer = csv.writer(f)
            labels = PyomicronLog.get_labels()
            writer.writerow(labels)
            log: PyomicronLog
            for log in self.logs:
                stats = log.get_stats()
                writer.writerow(stats)
                pass
        pass


class ProcessParameters:
    """
    Represents data in pyomicron run directory except what's in pyomicron.log and condor logs
    """
    def __init__(self, path=None, logger=None):
        """
        :param Path|str path: path to directory to process
        :param logging.logger logger: paret's logger to use
        """
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.status = ''
        self.available_trig_segs = SegmentList()
        self.seg_file = None
        self.seg_file_seg = SegmentList()
        self.param_segs = SegmentList()
        self.dag_info_list = list()
        self.bad_channel_list = list()
        self.available_trig_len = 0
        self.nerchan = 0

    def proc_params(self):
        """
        Find any Omicron parameter files inside path.
        Compare channels and times with triggers published
        :return str:  status ok, no analyzable segments, mising triggers
        """
        self.logger.log(VERBOSE, f'Checking {self.path.name}')
        ermsg = ''
        seg_file = self.path / 'segments.txt'
        if seg_file.is_file():
            self.seg_file = seg_file
            self.seg_file_seg = read_segfile(seg_file)
            seg_len = abs(self.seg_file_seg[0])
        else:

            seg_len = 0
            ermsg += "no segments.txt"

        self.dag_info_list = find_and_read_dag(self.path, logger=self.logger)
        for dag_info in self.dag_info_list:
            self.logger.log(VERBOSE, f'Omicron job segment: {dag_info["segment"]} '
                                     f'parameter file {dag_info["omicron_param"]}')

            nchan = 0
            self.nerchan = 0
            erchans = dict()
            param_file = dag_info['omicron_param']
            start = dag_info['segment'][0]
            end = dag_info['segment'][1]
            param_seg_len = abs(dag_info['segment'])

            chans = chans_from_parameters(param_file)
            nchan += len(chans)
            self.logger.debug(f'Checking {param_file.name} {len(chans)} channels')

            for cn, chan in enumerate(chans):
                try:
                    self.available_trig_segs = find_trig_seg(chan, start, end)
                    if len(self.available_trig_segs) == 0:
                        self.nerchan += 1
                        tseg_key = 'None'
                        if tseg_key in erchans.keys():
                            erchans[tseg_key].append(chan)
                        else:
                            erchans[tseg_key] = [chan]
                        ermsg += (f'path: {self.path.name} chan: {chan}, {start} - {end}, '
                                  f'no triggers found, seg len: {param_seg_len} \n')
                    else:
                        tseg_key = str(self.available_trig_segs)
                        tseg_len = abs(self.available_trig_segs[0])
                        self.available_trig_len = tseg_len

                        self.logger.debug(f'{cn}) Checking {chan} {len(tseg_key)} trigger segments {tseg_key}, \n'
                                          f'     chan trig len: {tseg_len}, seg len: {param_seg_len} ')
                        if abs(tseg_len - param_seg_len) > 1:
                            self.nerchan += 1
                            if tseg_key in erchans.keys():
                                erchans[tseg_key].append(chan)
                            else:
                                erchans[tseg_key] = [chan]
                            if len(self.bad_channel_list) == 0:
                                ermsg += (f'path: {self.path.name} chan: {chan}, {start} - {end}, '
                                          f'triggers missing trig len: {tseg_len}, seg len: {seg_len} \n')
                            self.bad_channel_list.append(chan)
                            self.available_trig_len = min(tseg_len, self.available_trig_len)

                except TypeError as ex:
                    p = f'{self.path.parent.name} / {self.path.name}'
                    self.logger.error(f'{ex} : {p} chan: {chan}, {start} - {end}')
                    pass
                pass  # good breakpoint location

            if ermsg == '':
                stat = f'OK. {nchan} channels in {param_file} parameter file have expected trigger file duration'
            else:
                stat = f'{self.nerchan} channels out of {nchan} are missing triggers\n'
                if self.logger.level >= VERBOSE:
                    stat = ermsg
                    klist = list(erchans.keys())
                    klist.sort()
                    stat += '\n'
                    for k in klist:
                        stat += f'{k}: {len(erchans[k])} channels\n'
            self.status = stat
        return self.status


class ProcParamStatistics:
    """
    Hlds a list of ProcessParameter object to create an output CSV file
    """
    def __init__(self, path=None, logger=None):
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.proc_params = list()

        if self.logger is None:
            self.logger = logging.getLogger('ProcParamStatistics')
            self.logger.setLevel(logging.ERROR)

    def add(self, param):
        """
        Add a new object to our list
        :param ProcessParameters param:
        :return: None
        """
        self.proc_params.append(param)

    def write_output(self):
        """
        Write out the output CSV file
        :return: None
        """
        pass


class OmicronParameter:
    """
    Represents the contents of the DAG's parameters file for a single0+-
    """
    def __init__(self, path=None, logger=None):
        self.path = Path(path) if path is not None else None
        self.logger = logger
        self.proc_segment = None
        self.parameter_files = None

        if self.logger is None:
            self.logger = logging.getLogger('OmicronParameter')
            self.logger.setLevel(logging.ERROR)


def find_and_read_dag(path: Path | str, logger=None):
    """
    :param  Logger|None logger: option to use callers logger
    :param Path|str path: path to pyomicron DAG, or condor directory or one above that
    :return list[OmicronParameter]: list describing the omicron jobs in

    We are looking or lines in the omicron dag like
    VARS Omicron_000 macroargument0="1417370284" macroargument1="1417370896"
        macroargument2="<dir>/parameters/parameters-0.txt"
    We want to save the process interval and path to omicron parameter files
    """
    var_matcher = re.compile('VARS.*macroargument0="(\\d+)".*macroargument1="(\\d+)".*'
                             'macroargument2="(.*parameters-\\d+.txt)"')
    thepath = Path(path)
    if logger is None:
        logger = logging.getLogger('find_and_read_dag')
        logger.setLevel(logging.ERROR)
    ret = list()
    if thepath is not None:
        if thepath.is_dir():
            srch = list(thepath.glob('omicron*dag'))
            if len(srch) == 0:
                condor_dir = thepath / 'condor'
                srch = list(condor_dir.glob('omicron*.dag'))
            if len(srch) == 0:
                srch = list(thepath.parent.glob('omicron*.dag'))
            if len(srch) == 0:
                logger.log(VERBOSE, f'No dag found at {thepath}')
            else:
                for dag in srch:
                    with dag.open() as f:
                        for line in f:
                            m = var_matcher.match(line)
                            if m is not None:
                                segment = Segment(int(m.group(1)), int(m.group(2)))
                                ret.append({'segment': segment, 'omicron_param': Path(m.group(3))})
    return ret
