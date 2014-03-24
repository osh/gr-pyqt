#!/usr/bin/env python
from plotter_base import *
class value_plot(plotter_base):
    def __init__(self, *args):
        plotter_base.__init__(self, *args)
        self.message_port_register_in(pmt.intern("reals"));
        self.set_msg_handler(pmt.intern("reals"), self.handler);

        # set up curves
        curve = Qwt.QwtPlotCurve("x(n)");
        curve.attach(self);
        self.curves.append(curve);
        curve.setPen( Qt.QPen(Qt.Qt.green) );
        
        self.curve_data = [([],[])]
        self.hist = [];

    def handler(self, msg):
        # get input
        x = float(pmt.to_python(msg))
        #x = pmt.to_double(msg)
        self.hist.append(x);

        # pass data
        self.curve_data[0] = (range(1,len(self.hist)), self.hist);

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)


