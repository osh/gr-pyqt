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

class select_input(gr.sync_block, QtGui.QComboBox):
    def __init__(self, blkname="select_input", opt=[], label="", *args):
        gr.sync_block.__init__(self,blkname,[],[])
        QtGui.QComboBox.__init__(self, *args)
        self.activated.connect(self.selection_changed);
        self.message_port_register_out(pmt.intern("pdus"));

        for o in opt:
            self.addItem(o)

    def start(self):
        self.selection_changed()
        return True

    def selection_changed(self):
        s = str(self.currentText().toUtf8())
        dt = pmt.to_pmt(s);
        self.message_port_pub(pmt.intern("pdus"), dt);

    def work(self, input_items, output_items):
        pass




