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
from gnuradio import gr
from PyQt4 import Qt, QtCore, QtGui
import pmt

class text_output(gr.sync_block, QtGui.QTextEdit):
    __pyqtSignals__ = ("updateText(QString)")
    def __init__(self, blkname="text_output", label="", *args):
        gr.sync_block.__init__(self,blkname,[],[])
        QtGui.QTextEdit.__init__(self, *args)
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handle_input);
        # connect the plot callback signal
        QtCore.QObject.connect(self,
                       QtCore.SIGNAL("updateText(QString)"),
                       self,
                       QtCore.SLOT("append(QString)"))

    def handle_input(self, msg):
        vec = pmt.cdr(msg)
        nvec = pmt.to_python(vec)
        s = str(nvec.tostring())
        self.emit(QtCore.SIGNAL("updateText(QString)"), s)

    def work(self, input_items, output_items):
        pass




