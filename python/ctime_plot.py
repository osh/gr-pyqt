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
        x = pmt.to_python(pmt.cdr(msg))
        
        # pass data
        self.curve_data[0] = (numpy.linspace(1,len(x),len(x)), numpy.imag(x));
        self.curve_data[1] = (numpy.linspace(1,len(x),len(x)), numpy.real(x));

        # trigger update
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)


