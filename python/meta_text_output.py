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
import numpy,pylab,pmt,pprint
from gnuradio import gr;
from PyQt4 import Qt, QtCore, QtGui

class meta_text_output(gr.sync_block, QtGui.QTextEdit):
    __pyqtSignals__ = ("updateText(int)")
    def __init__(self, blkname="meta_text_output", label="", *args):
        QtGui.QTextEdit.__init__(self, *args)
        gr.sync_block.__init__(self,blkname,[],[])
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handle_input);
        # connect the plot callback signal
        QtCore.QObject.connect(self,
                       QtCore.SIGNAL("updateText(int)"),
                       self.updateText)

    def handle_input(self, msg):
        meta = pmt.car(msg);
        meta_dict = pmt.to_python(meta);
        self.s = str(pprint.pformat(meta_dict))
        self.emit(QtCore.SIGNAL("updateText(int)"), 0)

    def updateText(self, a):
        self.setText(self.s);
        return True

    def work(self, input_items, output_items):
        pass




