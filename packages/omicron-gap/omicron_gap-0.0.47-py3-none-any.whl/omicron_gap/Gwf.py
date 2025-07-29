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
Class representing a gravitational wave file
"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import logging
from pathlib import Path

from LDAStools import frameCPP
import LDAStools


class Gwf:

    chan_list: list[str] | None
    proc_chan_list: list[str] | None
    adc_chan_list: list[str] | None
    toc: frameCPP.FrTOC | None
    path: Path | None
    stream: frameCPP.IFrameFStream | None

    def __init__(self, path=None, logger=None):
        """

        :type logger: logging.Logger
        :type path: str|Path
        """
        self.path = None if path is None else Path(path)
        self.stream = None
        self.toc = None
        self.adc_chan_list = None
        self.proc_chan_list = None
        self.chan_list = None

        if logger is None:
            logging.basicConfig()
            self.logger = logging.getLogger("GWF")
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger
        self.logger: logging.Logger

    def get_toc(self) -> LDAStools.frameCPP.FrTOC:
        if self.toc is None:
            if self.stream is None:
                if self.path is None:
                    raise ValueError('Unable to retrieve GWF channel list. No path set')
                self.stream = frameCPP.IFrameFStream(str(self.path.absolute()))
            self.toc = self.stream.GetTOC()
        return self.toc

    def get_channel_list(self) -> list[str]:

        if self.chan_list is not None:
            ret = self.chan_list
        else:
            ret = list()
            adc_list: list[str] = self.get_adc_list()
            if len(adc_list) > 0:
                ret.extend(adc_list)
            proc_list: list[str] = self.get_proc_list()
            if proc_list is not None:
                ret.extend(proc_list)
            self.chan_list = None
        return ret

    def get_proc_list(self) -> list[str]:
        if self.proc_chan_list is None:
            self.proc_chan_list = self.get_toc().GetProc()
        return self.proc_chan_list

    def get_adc_list(self) -> list[str]:
        if self.adc_chan_list is None:
            self.adc_chan_list = self.get_toc().GetADC()
        return self.adc_chan_list

    def get_frvect_data(self, chan: str) -> dict:
        if chan in self.get_adc_list():
            frdata = self.stream.ReadFrAdcData(0, chan)
        elif chan in self.get_proc_list():
            frdata = self.stream.ReadFrProcData(0, chan)
        else:
            raise ValueError(f'Channel {chan} not found in current frame {self.path.name}')
        ret = dict()
        data = frdata.data.pop()
        if data.nDim > 1:
            raise ValueError(f'We only support 1 dimensional channels (timeseries) {chan} has nÎim = {data.nDim}')

        dim = data.GetDim(0)
        ret["dtype"] = data.GetType()
        ret["dtype_str"] = get_data_type_name(ret["dtype"])
        ret["dx"] = dim.GetDx()
        ret["unitX"] = dim.GetUnitX()

        ret["bps"] = get_data_type_size(ret["dtype"])
        ret["fs"] = 1 / ret["dx"] if ret["dx"] > 0 else 0
        ret["data_rate"] = ret["bps"] * ret["fs"]

        return ret


def get_data_type_name(dtype):
    """ SEE APPENDIX C. FrVect Data Types

    :param dtype: (int) internal data type
    :return: (str) name of data type eg: "REAL_8"
   """
    type2str = {
        frameCPP.FrVect.FR_VECT_C: 'CHAR',
        frameCPP.FrVect.FR_VECT_2S: 'INT_2S',
        frameCPP.FrVect.FR_VECT_4S: 'INT_4S',
        frameCPP.FrVect.FR_VECT_8S: 'INT_8S',
        frameCPP.FrVect.FR_VECT_4R: 'REAL_4',
        frameCPP.FrVect.FR_VECT_8R: 'REAL_8',
        frameCPP.FrVect.FR_VECT_8C: 'COMPLEX_8',
        frameCPP.FrVect.FR_VECT_16C: 'COMPLEX_16',
        frameCPP.FrVect.FR_VECT_STRING: 'STRING',
        frameCPP.FrVect.FR_VECT_1U: 'CHAR_U',
        frameCPP.FrVect.FR_VECT_2U: 'INT_2U',
        frameCPP.FrVect.FR_VECT_4U: 'INT_4U',
        frameCPP.FrVect.FR_VECT_8U: 'INT_8U',
    }
    return type2str[dtype]


def get_data_type_size(dtype):
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
    return type2size[dtype]
