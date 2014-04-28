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
from plotter_base import *
class time_hist(plotter_base):
    def __init__(self, label="", *args):
        plotter_base.__init__(self, blkname="time_hist", label=label, *args)
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
                    print "unsupported pdu type in to pyqt.time_hist, please add the correct converted function"
            
        # pass data
        (a,b) = numpy.histogram(x, 100);
        self.curve_data[0] = (b,a);

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)


