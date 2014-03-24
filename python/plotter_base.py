#!/usr/bin/env python
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




