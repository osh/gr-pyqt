#!/usr/bin/env python
from plotter_base import *
class const_plot(plotter_base):
    def __init__(self, *args):
        plotter_base.__init__(self, *args)
        self.message_port_register_in(pmt.intern("cpdus"));
        self.set_msg_handler(pmt.intern("cpdus"), self.handler);


        # set up curve
        curve = Qwt.QwtPlotCurve("Plot 0");
        curve.attach(self);
        self.curves.append(curve);

        noline = True
        if(noline):
            curve.setStyle(Qwt.QwtPlotCurve.NoCurve);
            curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.XCross,
                                      Qt.QBrush(),
                                      #Qt.QPen(Qt.Qt.darkMagenta),
                                      Qt.QPen(Qt.Qt.green),
                                      Qt.QSize(1, 1)))

        self.curve_data = [([], [])];

    def handler(self, msg):
        # get input
        meta = pmt.car(msg);
        samples = pmt.cdr(msg);
        x = numpy.array(pmt.c32vector_elements(samples), dtype=numpy.complex64)
        
        # trigger update
        self.curve_data[0] = (numpy.real(x), numpy.imag(x));
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)


