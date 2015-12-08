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
import pylab
import numpy
from PyQt4 import Qt, QtCore, QtGui
import pmt,pprint

class range_input(gr.sync_block, QtGui.QGroupBox):
    def __init__(self, blkname="text_input", label="", *args):
        gr.sync_block.__init__(self,blkname,[],[])
        QtGui.QGroupBox.__init__(self, *args)
        self.filemax = 0;
        self.message_port_register_in(pmt.intern("file_range"));
        self.message_port_register_out(pmt.intern("range"));

        self.lay = QtGui.QGridLayout()
        self.setLayout(self.lay)
        self.scroll = QtGui.QScrollBar(Qt.Qt.Horizontal)
        self.laStart = QtGui.QLabel("Start Sample:")
        self.leStart = QtGui.QLineEdit("0")
        self.laLen = QtGui.QLabel("Sample Length:")
        self.leLen   = QtGui.QLineEdit("4096")

        self.lay.addWidget(self.scroll, 0, 0, 1, 4)
        self.lay.addWidget(self.laStart, 1, 0)
        self.lay.addWidget(self.leStart, 1, 1)
        self.lay.addWidget(self.laLen, 1, 2)
        self.lay.addWidget(self.leLen, 1, 3)

        self.leStart.returnPressed.connect(self.box_changed)
        self.leLen.returnPressed.connect(self.box_changed)
        self.scroll.sliderMoved.connect(self.slider_changed)
        self.set_msg_handler(pmt.intern("file_range"), self.set_file_range)
 
        self.box_changed()
        self.scroll.setFocusPolicy(QtCore.Qt.StrongFocus)
   
    def set_file_range(self,msg):
        (s,e) = pmt.to_python(msg)
        self.filemax = e
        goode = self.filemax - int(eval(str(self.leLen.text().toUtf8())))
        self.scroll.setMaximum(goode)
        self.scroll.setMinimum(s)


        # trigger a plot...
        self.values_changed()

    def start(self):
        return True

    def box_changed(self):
        startval = int(eval(str(self.leStart.text().toUtf8())))
        self.scroll.setValue(startval)
        lenval = int(eval(str(self.leLen.text().toUtf8())))
        goode = self.filemax - lenval
        self.scroll.setMaximum(goode)
        print lenval
        self.scroll.setSingleStep(lenval/2.0)
        self.scroll.setSingleStep(lenval)
        self.values_changed()

    def slider_changed(self):
        startval = self.scroll.value()
        self.leStart.setText(str(startval))
        self.values_changed()


    def values_changed(self):
        (s,l) = map(lambda x: pmt.from_long(int(eval(str(x.text().toUtf8())))),[self.leStart,self.leLen])
        self.message_port_pub(pmt.intern("range"), pmt.cons(s,l))

    def work(self, input_items, output_items):
        pass




