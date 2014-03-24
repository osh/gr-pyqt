#!/usr/bin/env python
from plotter_base import *
class cpower_plot(plotter_base):
    def __init__(self, *args):
        plotter_base.__init__(self, *args)
        self.message_port_register_in(pmt.intern("cpdus"));
        self.set_msg_handler(pmt.intern("cpdus"), self.handler);

        # set up curves
        curve = Qwt.QwtPlotCurve("Power");
        curve.attach(self);
        self.curves.append(curve);
        curve.setPen( Qt.QPen(Qt.Qt.green) );
        
        self.curve_data = [([],[])];

    def handler(self, msg):
        # get input
        meta = pmt.car(msg);
        samples = pmt.cdr(msg);
        x = numpy.array(pmt.c32vector_elements(samples), dtype=numpy.complex64)
        x = x * x.conjugate();

        # pass data
        self.curve_data[0] = (numpy.linspace(1,len(x),len(x)), numpy.real(x));

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)


