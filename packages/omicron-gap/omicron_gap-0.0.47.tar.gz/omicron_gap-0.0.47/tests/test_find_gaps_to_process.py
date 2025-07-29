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
""""""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

from omicron_gap.gap_utils import get_gps_day, get_default_ifo, find_segs_to_process


def test_find_segs_to_process():
    ifo, host = get_default_ifo()
    ifo = 'L1' if ifo is None else ifo
    if 'areeda' in host or 'caltech.edu' in host:
        config = '/home/detchar/omicron/online/l1-channels.ini'
        start, end = get_gps_day()
        gap = find_segs_to_process(config, ifo, 'LOW2', start, end)
        assert gap is not None
