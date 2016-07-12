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
    def __init__(self,filename,filetype="complex64"):
        gr.sync_block.__init__(self,"file_message_source",[],[])
        self.filename = filename
        self.set_filetype(filetype)
        self.F = None

        # set up message ports
        self.message_port_register_out(pmt.intern("file_range"));
        self.message_port_register_in(pmt.intern("range"));
        self.message_port_register_in(pmt.intern("file_type"));
        self.message_port_register_in(pmt.intern("file_open"));
        self.message_port_register_out(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("range"), self.range_received)
        self.set_msg_handler(pmt.intern("file_type"), self.filetype_received)
        self.set_msg_handler(pmt.intern("file_open"), self.file_open)

    def set_filetype(self, filetype):
        self.force_complex = False
        if(filetype[0:2] == 'c_'):
            self.force_complex = True
            filetype = filetype[2:]
         
        # store locals
        arr = numpy.array([1], dtype=filetype)
        if self.force_complex:
            (self.filetype, self.itemsize) = (filetype, 2*arr.itemsize)
        else:
            (self.filetype, self.itemsize) = (filetype, arr.itemsize)
        self.update_file_range()

    def start(self):
        try:
            self.F = open(self.filename, 'rb')
            self.F.seek(0, os.SEEK_END)
            (s,l) = (0,self.F.tell()/self.itemsize)
            self.message_port_pub(pmt.intern("file_range"), 
                pmt.cons(pmt.from_long(s),pmt.from_long(l)))
            return True
        except:
            return False

    def stop(self):
        self.F.close()
        self.F = None

    def range_received(self, msg):
        (s,l) = pmt.to_python(msg)
        self.f_range = (s,l)
        self.update_file_range()

    def filetype_received(self, msg):
        filetype = pmt.to_python(msg)
        self.set_filetype(filetype)
        self.update_file_range()

    def file_open(self, msg):
        print "open"
        filename = pmt.to_python(msg)
        self.filename = filename    
        self.start()
        self.update_file_range()

    def update_file_range(self):
        try:
            (s,l) = self.f_range
            meta = {"start":s, "len":l, "end":s+l, "filename":self.filename}
            self.F.seek(s*self.itemsize)
            if self.force_complex:
                vec = numpy.fromfile(self.F, dtype=self.filetype, count=2*l, sep='')
                vec = vec[0::2] + 1j*vec[1::2]
            else:
                vec = numpy.fromfile(self.F, dtype=self.filetype, count=l, sep='')
            vec = numpy.array(vec, dtype="complex64")
            self.message_port_pub(pmt.intern("pdus"), 
                pmt.cons(
                    pmt.to_pmt(meta),
                    pmt.to_pmt(vec) ))
        except:
            pass
        
    def work(self, input_items, output_items):
        pass




