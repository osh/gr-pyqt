#!/usr/bin/env python
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


