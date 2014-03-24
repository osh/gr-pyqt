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
from scipy import signal
import pylab

from PyQt4 import Qt, QtCore
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
import pmt

class plotter_base(gr.sync_block, Qwt.QwtPlot):
    __pyqtSignals__ = ("updatePlot(int)")

    def __init__(self, blkname="pyqt_plotter", label="", *args):
        gr.sync_block.__init__(self,blkname,[],[])
        Qwt.QwtPlot.__init__(self, *args)

        # set up label if desired
        if not label == "":
            self.setTitle(label)

        # set up background etc
        self.setCanvasBackground(Qt.Qt.black)
        self.alignScales()

        # curve storage
        self.curves = [];
        self.curve_data = [];

        # connect the plot callback signal
        QtCore.QObject.connect(self,
                       QtCore.SIGNAL("updatePlot(int)"),
                       self.do_plot)

    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(
                    Qwt.QwtAbstractScaleDraw.Backbone, False)

    def do_plot(self, a):
        # set curve data for known curves
        for i in range(0,min(len(self.curves),len(self.curve_data))):
            (x,y) = (self.curve_data[i][0], self.curve_data[i][1]);
            self.curves[i].setData(x,y);
        self.replot();
        self.show();

    def work(self, input_items, output_items):
        pass




