#!/usr/bin/env python
#
# Copyright 2015 Tim O'Shea
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
import pylab,numpy,os
import pmt,pprint
from PyQt4 import Qt, QtCore, QtGui

class file_message_sink(gr.sync_block, QtGui.QPushButton):
    def __init__(self,filename="/tmp/out.dat",filetype="complex64",label="Save", *args):
        gr.sync_block.__init__(self,"file_message_sink",[],[])

        # GUI Set up
        QtGui.QPushButton.__init__(self, QtGui.QIcon.fromTheme("open"), label, *args)
        self.clicked.connect(self.save_file)

        # set up message ports
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.rx_pdu)
        self.msg = None

    def start(self):
        self.msg = None

    def rx_pdu(self, msg):
        msg = pmt.to_python(msg)
        self.msg = msg

    def save_file(self):
        fn = str(QtGui.QFileDialog.getSaveFileName(self, "Open Dataset").toUtf8())
        print "saving",fn
        f = open(fn, "w")
        x = self.msg[1]
        print type(x)
        x.tofile(f)
        f.flush()
        f.close()




