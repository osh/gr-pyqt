#!/usr/bin/env python
#
# Copyright 2015 Tim O'Shea
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
import pylab,numpy,os
import pmt,pprint

class file_message_source(gr.sync_block):
    def __init__(self,filename):
        gr.sync_block.__init__(self,"file_message_source",[],[])
        self.message_port_register_out(pmt.intern("file_range"));
        self.message_port_register_in(pmt.intern("range"));
        self.message_port_register_out(pmt.intern("pdus"));
        self.filename = filename
        self.itemsize = gr.sizeof_gr_complex
        self.F = None
        self.set_msg_handler(pmt.intern("range"), self.range_received)

    def start(self):
        self.F = open(self.filename, 'rb')
        self.F.seek(0, os.SEEK_END)
        (s,l) = (0,self.F.tell()/self.itemsize)
        self.message_port_pub(pmt.intern("file_range"), 
            pmt.cons(pmt.from_long(s),pmt.from_long(l)))
        return True

    def stop(self):
        self.F.close()
        self.F = None

    def range_received(self, msg):
        (s,l) = pmt.to_python(msg)
        meta = {"start":s, "len":l, "end":s+l, "filename":self.filename}
        self.F.seek(s*self.itemsize)
        vec = numpy.fromfile(self.F, dtype=numpy.complex64, count=l, sep='')
        self.message_port_pub(pmt.intern("pdus"), 
            pmt.cons(
                pmt.to_pmt(meta),
                pmt.to_pmt(vec) ))
        
    def work(self, input_items, output_items):
        pass




