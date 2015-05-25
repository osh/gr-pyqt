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
import pmt

class stream_lambda(gr.sync_block):
    def __init__(self, fn, insig=[numpy.complex64], outsig=[numpy.complex64]):
        gr.sync_block.__init__(self,"stream_lambda",insig,outsig)
        self.set_fn(fn)
        self.lvars = {}

    # signature should be:  (output_stream_items) = lambda input_items, output_stream_index: ....
    def set_fn(self,fn):
        self.fn = fn

    def work(self, input_items, output_items):
        n_out = 0;
        for i in range(0,len(output_items)):
            o = self.fn(input_items, i)
            output_items[i][0:len(o)] = o[:]
            if(n_out == 0 or n_out == len(o)):
                n_out = len(o)
            else:
                raise Exception("Streams must produce same lengths for now with the current stream lambda block interface!")
        return n_out




