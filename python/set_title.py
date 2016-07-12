#!/usr/bin/env python
#
# Copyright 2016 Tim O'Shea
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
import numpy
from gnuradio import gr;
import pylab
import numpy
from PyQt4 import Qt, QtCore, QtGui
import pmt

class set_title(gr.sync_block):
    def __init__(self, blkname="set_title", prefix="Title: ", parent=None):
        gr.sync_block.__init__(self,blkname,[],[])
        self.message_port_register_in(pmt.intern("name"));
        self.set_msg_handler(pmt.intern("name"), self.handler)
        self.prefix = prefix
        self.parent = parent
        self.n = ""

    def handler(self,msg):
        try:
            self.n = str(pmt.to_python(msg))
            self.parent.setWindowTitle(self.prefix + self.n)
        except:
            pass

    def work(self, input_items, output_items):
        pass




