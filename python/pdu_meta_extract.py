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
import pmt
from gnuradio import gr
class pdu_meta_extract(gr.sync_block):
    def __init__(self, key):
        gr.sync_block.__init__(self,"pdu_meta_extract",[],[])
        self.key = key;
        self.outport = pmt.intern("values");
        self.message_port_register_in(pmt.intern("pdus"));
        self.message_port_register_out(self.outport);
        self.set_msg_handler(pmt.intern("pdus"), self.handler);

    def handler(self, msg):
        # get input
        meta = pmt.car(msg);
        samples = pmt.cdr(msg);

        # ensure we have a dictionary
        assert(pmt.is_dict(meta))
        #print pmt.to_python(pmt.dict_keys(meta));

        # get the value from dict and publish it
        val = pmt.dict_ref(meta, self.key, pmt.PMT_NIL)
        self.message_port_pub(self.outport, val);

    def work(self, input_items, output_items):
        pass


