# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2021 Joseph Areeda <joseph.areeda@ligo.org>
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

"""Classes used to define condor files a Omicron project"""

import logging
from pathlib import Path

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__myname__ = 'Omicrondag'


class OmicronError(RuntimeError):
    """Base class for exceptions in this module."""
    pass


class OmicronConfigError(OmicronError):
    """Omicron config file processing error.
    In most cases errors will already be logged"""
    pass


class OmicronDag:
    """ Used to define an htCondor DAG
    We assemble everything here"""

    def __init__(self, group=None, outdir=None):
        #: each task object
        self.tasks = dict()
        #: define any parent-child relationship
        self.parents = dict()
        #: Base directory for this event
        self.outdir = outdir
        #: directory holding dag description file and condor dag output
        self.dagdir = None
        self.group = group
        self.dag_path = None
        self.retry = 0

        # create a default logger, but expect it to be overridden
        logging.basicConfig()
        self.logger = logging.getLogger(__myname__)
        self.logger.setLevel(logging.CRITICAL)

    def add_parent_child(self, parent, child):
        """
        Set the parent child relations ship between two tasks.
        A parent must complete before a child starts.
        By default if a parent failes (non-zero return code)
        its children will not run.

        :param str parent:  Parent task name
        :param str child: Child task name
        """
        if parent in self.parents.keys():
            self.parents[parent].append(child)
        else:
            self.parents[parent] = [child]

    def add_task(self, task):
        self.tasks[task.name] = task

    def set_retry(self, retry_str):
        """
        The default retry for jobs in the DAG
        :param retry_str: should be an int or str
        """
        try:
            self.retry = int(retry_str)
        except ValueError:
            self.logger.error('Invalid value for retrying jobs[{}]'.format(retry_str))

    def set_outdir(self, outdir):
        """
        Specify directory for all results for this event
        """
        self.outdir = Path(outdir)
        if not self.outdir.exists():
            self.outdir.mkdir(parents=True, mode=0o755)
        self.dagdir = self.outdir.joinpath('dag')
        if not self.dagdir.exists():
            self.dagdir.mkdir(parents=True, mode=0o755)

    def write_dag(self):
        """
        Create the HTCondor files to handle this job
        """
        if self.outdir is None or not self.outdir.exists():
            raise OmicronConfigError('Cannot write DAG because valid directory not set or does not exist')
        self.logger.info(f'Writing DAG and submit files for {self.group} to {self.outdir}')

        dag_name = f'omicron-gap-{self.group}.dag'
        self.dag_path = self.dagdir / dag_name

        # write the task stuff first
        for task in self.tasks.values():
            task.outdir = self.dagdir
            if task.needs_submit:
                task.write_submit()

        with open(self.dag_path, 'w') as dagfp:

            for name, task in self.tasks.items():
                job_stmt = task.get_job_stmt()
                print(job_stmt, file=dagfp)
                retry = task.retry if task.retry >= 0 else self.retry
                if retry > 0:
                    print(f'RETRY {task.name} {retry}', file=dagfp)
                if task.vars:
                    print(f'VARS {task.name} {task.vars}', file=dagfp)

            for mom, kids in self.parents.items():
                print(f'PARENT {mom} CHILD {" ".join(kids)}', file=dagfp)

            # visualize the task relationships
            dotpath = str(Path(self.dagdir) / f'{self.group}.dot')
            print(f'DOT {dotpath}', file=dagfp)


class OmicronTask:
    """
    Class representing an individual job
    """

    def __init__(self, name=None, logger=None, outdir=None, group=None, needs_submit=True):
        self.parents = list()       # text .dag files use parent parameter
        self.children = list()      # API workflows specify children
        self.name = name            # task identifier (alphanum+_ first char not numeric)
        self.group = group
        self.outdir = outdir        # path to task subdirectory or this run
        self.classads = dict()      # separate classads these will go into the submit file
        self.vars = None            # Variable that go into the DAG file as a VARS statement
        self.retry = -1             # how many times should condor try
        self.extra = ''             # user specified lines to be copied directly
        self.subfile = None         # the submit file written
        self.needs_submit = needs_submit

        if logger is not None:
            logging.basicConfig()
            self.logger = logging.getLogger(__myname__)
            self.logger.setLevel(logging.CRITICAL)

    def add_classad(self, key, val):
        """
        addc key value pair to our classad dictionary
        """
        self.classads[key] = val

    def update(self, classads):
        """
        Add all entries from input to our classads
        :param dict classads: multiple classads (key:val)
        :return: None
        """
        if classads:
            self.classads.update(classads)
        else:
            self.logger.error('Omicron task update called with unusable argument')

    def write_submit(self):
        """
        Create the subdirectory, if needed, and condor submit file for this task
        """

        self.logger.debug(f'Write condor submit file. Task: {self.name}, Group: {self.group}')

        odir = self.outdir
        if not odir:
            raise OmicronConfigError(f'Attempt to write task {self.name} {self.group} Condor submit '
                                     'file for but output directory not set')
        odir = Path(odir)
        odir.mkdir(parents=True, mode=0o775, exist_ok=True)

        outfile_base = str(self.outdir / f'{self.group}-{self.name}')
        self.subfile = Path(outfile_base + '.submit')
        subfile = Path(self.subfile)
        subfile.parent.mkdir(mode=0o775, parents=True, exist_ok=True)

        for otyp in ['.output', '.error', '.log']:
            procnum = '-$(Process)' if 'queue' in self.classads.keys() else ''
            ofile = outfile_base + procnum + otyp[0:4]
            self.add_classad(otyp[1:], ofile)

        with open(subfile, 'w') as subfp:
            queue_stmt = 'queue 1'
            for key, val in sorted(self.classads.items()):
                if key == 'queue':
                    queue_stmt = f'{key} {str(val)}'
                else:
                    print(f'{key} = {str(val)}', file=subfp)
            if self.extra != '':
                print(self.extra, file=subfp)

            # queue statement must be last
            print(queue_stmt, file=subfp)

    def add_extras(self, extras):
        """Update classads with constant values"""
        if self.extra != '' and not self.extra.endswith('\n'):
            self.extra += '\n'
        self.extra += extras
        if not extras.endswith('\n'):
            self.extra += '\n'

    def get_job_stmt(self):
        """Create the statement for the DAG to inlucde this Job"""
        ret = f'JOB {self.name} {self.subfile}'
        return ret


class OmicronScript(OmicronTask):
    """
    Class representing pre and post scripts in a DAG
    """
    def __init__(self, is_post, parent, script, arguments, **kwargs):
        super().__init__(needs_submit=False, **kwargs)
        self.is_post = is_post
        self.parent = parent
        self.script = script
        self.arguments = arguments

    def get_job_stmt(self):
        styp = 'POST' if self.is_post else 'PRE'
        ret = f'SCRIPT {styp} {self.parent.name} {self.script} {self.arguments}'
        return ret


class OmicronSubdag(OmicronTask):
    """
    class for connecting subdag to dag
    """
    def __init__(self, name, dag_path, logger=None, **kwargs):
        super().__init__(name=name, logger=logger, needs_submit=False, **kwargs)
        self.dag_path = dag_path

    def get_job_stmt(self):
        ret = f'SUBDAG EXTERNAL {self.name} {self.dag_path}'
        return ret
