#!/usr/bin/env python
import numpy
from gnuradio import gr;
from scipy import signal
import pylab

from PyQt4 import Qt, QtCore
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
import pmt

class plotter(gr.sync_block, Qwt.QwtPlot):
    __pyqtSignals__ = ("updatePlot(int)")

    def __init__(self, *args):
        gr.sync_block.__init__(self,"plotter",[],[])
        Qwt.QwtPlot.__init__(self, *args)

        # set up background etc
        self.setCanvasBackground(Qt.Qt.black)
        self.alignScales()

        # set up line/plot style
        self.curve = Qwt.QwtPlotCurve("Data Moving Right")
        self.curve.attach(self)
        noline = True
        if(noline):
            self.curve.setStyle(Qwt.QwtPlotCurve.NoCurve);
            self.curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.XCross,
                                      Qt.QBrush(),
                                      #Qt.QPen(Qt.Qt.darkMagenta),
                                      Qt.QPen(Qt.Qt.green),
                                      Qt.QSize(1, 1)))

        self.message_port_register_in(pmt.intern("cpdus"));
        self.message_port_register_out(pmt.intern("cpdus"));
        self.set_msg_handler(pmt.intern("cpdus"), self.handler);

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
        self.curve.setData(self.x, self.y)
        self.replot();
        self.show();

    def handler(self, msg):
        # get input
        meta = pmt.car(msg);
        samples = pmt.cdr(msg);
        x = numpy.array(pmt.c32vector_elements(samples), dtype=numpy.complex64)
        
        # trigger update
        self.x = numpy.real(x);
        self.y = numpy.imag(x);
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)

    def work(self, input_items, output_items):
        pass




