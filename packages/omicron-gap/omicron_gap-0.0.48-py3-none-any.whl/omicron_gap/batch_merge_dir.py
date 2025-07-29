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

"""
Checks if already merged, updates old format ligolw XML, calls merge with gaps, then confirms trigger counts
"""
import shutil
import time
start_time = time.time()

from gwpy.table import EventTable

import argparse
import logging
from pathlib import Path
import re
import subprocess
import sys
from ._version import __version__


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'batch_merge_dir'
epilog = """Input is directory path, to top trigger directory, channel, metric day and trigger type (root, h5, xml),
and the output directory path.
"""

log_format = "%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format)
formatter = logging.Formatter(log_format)
logger = logging.getLogger(__process_name__)
logger.setLevel(logging.DEBUG)

fpat = '^(.+)-(\\d+)-(\\d+).(.+)$'
fmatch = re.compile(fpat)


def error_exit(ecode, channel, day, ext, ermsg, outdir):
    """Fatal error occurred log it and exit"""
    error_file = outdir / 'failure' / f'{channel}-{day}-{ext}.err'
    error_file.parent.mkdir(exist_ok=True, parents=True)
    with error_file.open('a') as erfp:
        print(ermsg, file=erfp)
    logger.debug(f'Fatal error: {ecode} - {ermsg}. Error written to {str(error_file.absolute())} ')
    sys.exit(ecode)


def get_exe(prog_name, channel, day, ext, outdir):
    ret = shutil.which(prog_name)
    if ret is None:
        path_guess = Path(sys.executable).parent / prog_name
        if path_guess.exists():
            ret = str(path_guess.absolute())
        else:
            error_exit(3, channel, day, ext, f'Prog: {prog_name} not found', outdir)
    return ret


def count_trigs(ext, flist):
    """
    Count the number of triggers in the list of files
    :param str ext:
    :param flist:
    :return:
    """
    count = 0
    duration = 0
    for path in flist:
        table = None
        if path.exists():
            m = fmatch.match(str(path.name))
            if m:
                dur = int(m.group(3))
                duration += dur
            if path.name.endswith('.h5'):
                table = EventTable.read(path, path='/triggers')
            elif path.name.endswith('.xml.gz') or path.name.endswith('.xml'):
                table = EventTable.read(path, tablename='sngl_burst')
            elif path.name.endswith('.root'):
                # reading root files fail if there is a : in the name
                table = EventTable.read(path, treename='triggers;1')

            count += 0 if table is None else len(table)
    return count, duration


def main():

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     epilog=epilog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    ingroup = parser.add_argument_group(title='Input definition')
    ingroup.add_argument('-i', '--indir', type=Path, help='Top level trigger directory for this IFO')
    ingroup.add_argument('-c', '--channel', help='Channel or trigger directory name')
    ingroup.add_argument('-d', '--day', type=int, help='5 digit metric day')
    ingroup.add_argument('-e', '--ext', help='extension to process (root, h5, xml)')

    outgroup = parser.add_argument_group('Output definition')
    outgroup.add_argument('-o', '--outdir', type=Path, help='Top directory for work')
    outgroup.add_argument('-l', '--logfile', type=Path, help='File to append log messages')

    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    if args.logfile:
        args.logfile.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        handler = logging.handlers.RotatingFileHandler(args.logfile.absolute(), maxBytes=(1048576 * 5), backupCount=4)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # debugging?
    logger.debug('{} called with arguments:'.format(__process_name__))
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    channel = args.channel
    day = str(args.day)
    ext = str(args.ext)
    indir = Path(args.indir) / channel / day
    outdir = Path(args.outdir)
    ready_dir = outdir / 'ready'
    ready_to_copy_flag = ready_dir / f'{ext}-{day}.txt'
    ready_to_copy_flag.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
    if ready_to_copy_flag.exists():
        logger.info(f'{channel}, {day}, {ext} is ready to replace original. Skipping.')
        sys.exit(9)

    trig_flist = list(indir.glob(f'*.{ext}*'))
    logger.debug(f'{len(trig_flist)} files of type {ext} found.')
    if len(trig_flist) == 0:
        error_exit(5, channel, day, ext, 'No triggers found', outdir)

    bkup_path = outdir / 'backup' / f'{ext}-{day}.tgz'
    if not bkup_path.exists():
        tstrt = time.time()
        bkup_path.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        logger.debug(f'Back up type: {ext} day: {day} to {bkup_path}')
        tar_exe = get_exe('tar', channel, day, ext, outdir)
        tar_cmd = [tar_exe, '-czf', str(bkup_path.absolute())]

        for trig in trig_flist:
            tar_cmd.append(trig.name)
        res = subprocess.run(tar_cmd, capture_output=True, cwd=indir)
        if res.returncode != 0:
            error_exit(2, channel, day, ext, f'tar failed for {ext} files in {indir.absolute()}. Return code: '
                                             f'({res.returncode}):\n{res.stderr.decode("utf-8")}', outdir)
        logger.info(f'{str(bkup_path.absolute())} created  in {time.time() - tstrt:.1f}s')

    tmp_dir = None
    if 'xml' in ext.lower():
        cvt_start = time.time()
        # copy them to a temp directory because we may have to modify them before
        tmp_dir = outdir / 'temp'
        tmp_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        upd_cmd = get_exe('ligolw_no_ilwdchar', channel, day, ext, outdir)
        merge_list = list()
        for infile in trig_flist:
            outfile = tmp_dir / infile.name
            shutil.copy(infile, outfile)
            res = subprocess.run([upd_cmd, outfile])
            if res.returncode != 0:
                ermsg = f'problem updating xml file {upd_cmd} returned {res.returncode}\n{res.stderr.decode("utf-8")}'
                error_exit(4, channel, day, ext, ermsg, outdir)
            merge_list.append(outfile)
        logger.info(f'ligolw files copied and updated to {str(tmp_dir.absolute())} in {time.time() - cvt_start:.1f}s')
    else:
        merge_list = trig_flist

    merge_start = time.time()
    merge_out_path = outdir / 'merged' / f'{ext}'

    if merge_out_path.exists():
        shutil.rmtree(merge_out_path)
    merge_logfile = merge_out_path / 'merge-with-gaps.log'
    merge_out_path.mkdir(mode=0o755, exist_ok=True, parents=True)
    merge_prog = get_exe('omicron-merge-with-gaps', channel, day, ext, outdir)

    merge_cmd = [merge_prog, '--out-dir', str(merge_out_path), '--log-file', str(merge_logfile), '-vvv']
    merge_cmd.extend(merge_list)
    merge_cmd_str = ''
    for c in merge_cmd:
        merge_cmd_str += str(c) + " "
    logger.debug(f'Merge command: {merge_cmd_str}')
    res = subprocess.run(merge_cmd, capture_output=True)
    if res.returncode != 0:
        ermsg = f'merge-with-gaps failed ({res.returncode})\n{res.stderr.decode("utf-8")}'
        error_exit(6, channel, day, ext, ermsg, outdir)
    logger.info(f'Merge-with-gaps succeeded. Results in {str(merge_out_path)}. Elapsed '
                f'{time.time() - merge_start:.1f}s')

    # Confirm merge
    in_trig_cnt, in_duration = count_trigs(ext, merge_list)
    out_flist = list(merge_out_path.glob(f'*.{ext}*'))
    out_trig_cnt, out_duration = count_trigs(ext, out_flist)
    if in_trig_cnt == out_trig_cnt and in_duration == out_duration:
        success_msg = f'{len(trig_flist)} {ext} files were merged into {len(out_flist)} ' \
                      f'containing {in_trig_cnt} triggers covering {in_duration} seconds\n' \
                      f'Trigger counts verified correct.\n\n' \
                      f'CSV: {len(trig_flist)}, {ext}, {len(out_flist)}, {in_trig_cnt}, {in_duration}'
        logger.info(success_msg)
        with ready_to_copy_flag.open('w') as rflag:
            print(success_msg, file=rflag)
            logger.info(f'Ready to replace flag created as {str(ready_to_copy_flag.absolute())}')

        if tmp_dir is not None:
            shutil.rmtree(tmp_dir)
            logger.debug(f'temp dir removed {str(tmp_dir.absolute())}')
        if len(trig_flist) == len(out_flist):
            logger.info('Merge verified but did not reduce file count. No copy script')
        elif len(trig_flist) > len(out_flist):
            ready_to_copy_script = ready_dir / f'{ext}-{day}.copy.sh'
            with ready_to_copy_script.open("w") as cscr:
                print(f'#!/bin/bash\n# update {channel} {ext} for {day}', file=cscr)
                print(f'\n# delete {len(trig_flist)} source files of type {ext}', file=cscr)
                for infile in trig_flist:
                    print(f'\\rm -f {infile.absolute()}', file=cscr)
                if tmp_dir is not None:
                    print('# We also have to delete the temporary directory used to update any old ligolw files.',
                          file=cscr)
                    for infile in merge_list:
                        print(f'\\rm -f {infile.absolute()}', file=cscr)

                print(f'\n# Move {len(out_flist)} merged files into the production directory', file=cscr)
                for outfile in out_flist:
                    print(f'mv {outfile.absolute()} {indir.absolute()}', file=cscr)
            dir_proessed_flag_script = ready_dir / 'add_dir_processed_flag.sh'
            dir_processed_file = indir / 'day_was_merged'
            with dir_proessed_flag_script.open('w') as dpfs:
                print('#!/bin/bash', file=dpfs)
                print('# create the file in the production trigger dir that signifies it has been processed', file=dpfs)
                print(f'\necho -n "metric_day_merge has processed this directory on " >{dir_processed_file.absolute()}\n'
                      f'date >>{dir_processed_file.absolute()}', file=dpfs)

    else:
        ermsg = f'Merge failed to confirm count. Input files had {in_trig_cnt} trigs {in_duration} secs, ' \
                f'output had {out_trig_cnt} over {out_duration} s'
        error_exit(7, channel, day, ext, ermsg, outdir)

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()
