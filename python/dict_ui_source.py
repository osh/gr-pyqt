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
from PyQt4 import Qt, QtCore, QtGui
import numpy
from gnuradio import gr;
import pylab,numpy,os
import pmt,pprint

class dict_ui_source(gr.sync_block, QtGui.QGroupBox):
    def __init__(self,defaults={"filename":"test.dat", "count":500},submit_text="Send", *args):
        gr.sync_block.__init__(self,"dict_ui_source",[],[])
        QtGui.QGroupBox.__init__(self, *args)

        # store locals
        self.defaults = defaults

        # Set up GUI bits
        self.labels = {}
        self.textinputs = {}
        self.lay = QtGui.QGridLayout(self)        
        #self.lay = QtGui.QVBoxLayout()        
        self.setWindowTitle("Many Controls")
        for k,v in defaults.iteritems():
            i = defaults.keys().index(k)
            lbl = QtGui.QLabel(k)
            txt = QtGui.QLineEdit(str(v))
            self.lay.addWidget(lbl, i, 0)
            self.lay.addWidget(txt, i, 1)
            self.labels[k] = lbl
            self.textinputs[k] = txt
        self.button = QtGui.QPushButton(str(submit_text))
        self.button.pressed.connect(self.button_clicked)
        self.lay.addWidget(self.button, len(defaults.keys()), 0, 1, 2)

        # set up message ports
        self.message_port_register_out(pmt.intern("pdus"));

    def button_clicked(self):
        print "clicked"
        meta = {}
        for k,v in self.textinputs.iteritems():
            try:
                meta[k] = int(str(v.text()))
            except:
                meta[k] = str(v.text())
        pprint.pprint(meta)
        vec = pmt.PMT_NIL
        self.message_port_pub(pmt.intern("pdus"), 
            pmt.cons( pmt.to_pmt(meta), pmt.PMT_NIL ))
        
    def work(self, input_items, output_items):
        pass




