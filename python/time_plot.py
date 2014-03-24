#!/usr/bin/env python
from plotter_base import *
class time_plot(plotter_base):
    def __init__(self, label="", *args):
        plotter_base.__init__(self, blkname="time_plot", label=label, *args)
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);

        # set up curves
        curve = Qwt.QwtPlotCurve("x(n)");
        curve.attach(self);
        self.curves.append(curve);
        curve.setPen( Qt.QPen(Qt.Qt.green) );
        
        self.curve_data = [([],[]), ([],[])];

    def handler(self, msg):
        # get input
        meta = pmt.car(msg);
        samples = pmt.cdr(msg);

        x = None
        if pmt.is_f32vector(samples):
            x = numpy.array(pmt.f32vector_elements(samples), dtype=numpy.float32)
        else:
            if pmt.is_s16vector(samples):
                x = numpy.array(pmt.f32vector_elements(samples), dtype=numpy.float32)
            else:
                if pmt.is_u8vector(samples):
                    x = numpy.array(pmt.u8vector_elements(samples), dtype=numpy.float32)
                else:
                    print "unsupported pdu type in to pyqt.time_plot, please add the correct converted function"
            
        # pass data
        self.curve_data[0] = (numpy.linspace(1,len(x),len(x)), x);

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)


