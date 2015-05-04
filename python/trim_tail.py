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
import pmt

class trim_tail(gr.sync_block):
    def __init__(self, max_item):
        self.max_item = max_item
        gr.sync_block.__init__(self,"message_trim_tail",[],[])
        self.message_port_register_in(pmt.intern("pdus"))
        self.message_port_register_out(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handler)   

    def handler(self, pdu):
        meta = pmt.car(pdu)
        vec = pmt.to_python(pmt.cdr(pdu))
        idx = numpy.argmax(numpy.abs(vec) > self.max_item)
        if(not idx == 0):
            vec = vec[0:idx]
        self.message_port_pub(pmt.intern("pdus"), pmt.cons( meta, pmt.to_pmt(vec) ) );

    def work(self, input_items, output_items):
        pass




