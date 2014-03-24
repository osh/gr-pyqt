#!/usr/bin/env python
from plotter_base import *
class ctime_plot(plotter_base):
    def __init__(self, label="", *args):
        plotter_base.__init__(self,blkname="ctime_plot", label=label, *args)
        self.message_port_register_in(pmt.intern("cpdus"));
        self.set_msg_handler(pmt.intern("cpdus"), self.handler);

        # set up curves
        curve = Qwt.QwtPlotCurve("Re");
        curve.attach(self);
        self.curves.append(curve);
        curve.setPen( Qt.QPen(Qt.Qt.red) );
        #curve.setPen( Qt.QPen(Qt.Qt.blue) );
        
        curve = Qwt.QwtPlotCurve("Im");
        curve.attach(self);
        self.curves.append(curve);
        curve.setPen( Qt.QPen(Qt.Qt.green) );

        self.curve_data = [([],[]), ([],[])];

    def handler(self, msg):
        # get input
        meta = pmt.car(msg);
        samples = pmt.cdr(msg);
        x = numpy.array(pmt.c32vector_elements(samples), dtype=numpy.complex64)
        
        # pass data
        self.curve_data[0] = (numpy.linspace(1,len(x),len(x)), numpy.imag(x));
        self.curve_data[1] = (numpy.linspace(1,len(x),len(x)), numpy.real(x));

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)


