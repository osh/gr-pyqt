#!/usr/bin/env python
#
# Copyright 2014 Tim O'Shea
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

class variable_text_input(gr.sync_block, QtGui.QLineEdit):
    def __init__(self, fn_update=None, blkname="text_input", val="", label="", *args):
        gr.sync_block.__init__(self,blkname,[],[])
        QtGui.QLineEdit.__init__(self, *args)
        self.returnPressed.connect(self.text_changed);
        self.message_port_register_out(pmt.intern("pdus"));
        self.fn_update = fn_update
        self.setText(str(val))

    def text_changed(self):
        s = self.text().toUtf8();
        #nvec = numpy.fromstring((s), dtype=numpy.uint8, count=len(s));
        #vec = pmt.to_pmt(nvec);
        print s
        self.fn_update(eval(str(s)))
        #self.message_port_pub(pmt.intern("pdus"), pmt.cons(pmt.PMT_NIL, vec));
        #self.clear();

    def work(self, input_items, output_items):
        pass




