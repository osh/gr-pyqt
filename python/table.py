#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr
from PyQt4 import Qt, QtCore, QtGui
import pmt

class table(gr.sync_block, QtGui.QTableWidget):
    updateTrigger = QtCore.pyqtSignal()
    """
    This is a PyQT-Table. It will be populated by PDU messages.
    For every new message, it would insert a new row, which might not be
    what you want. So instead, if you specify a "row identifier", that will act
    as  a unique id (as for a normal Database), so that you can update rows
    in case the meta field dict values match.
    If you specify a list of strings as "columns" the meta field will be filtered
    for those in order to just extract the desired values and feed them into the table.

    TODO: give users the chance to NOT filter the meta field
    TODO: give users the chance to NOT specify a unique id

    Approach:
    1. Get the message and extract meta field
    2. Assert that the desired row identifier exists
    3. Every other meta field entry will be put into the table
    4. The "columns" parameter can be used to filter out other meta field entries.
    """
    def __init__(self, blkname="table", label="", row_id="", columns=[], *args):
        gr.sync_block.__init__(self,
            name="blkname",
            in_sig=[],
            out_sig=[])
        QtGui.QTableWidget.__init__(self, *args)
        self.message_port_register_in(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handle_input)
        self.scroll_to_bottom = True
        self.updateTrigger.connect(self.updatePosted)

        ## table setup

        # if both row_id and columns are set
        # assert that row_id is present in the list of columns
        # and pre-set column headers
        if row_id is not None:
            self.row_id = row_id
            self.ids = {} # mapping aid for identifiers
            # set identifier column
            item = QtGui.QTableWidgetItem(row_id)
            self.insertColumn(0)
            self.setHorizontalHeaderItem(0, item)
            self.column_dict = {} # mapping aid for column indices
            self.column_dict[self.row_id] = 0

            if columns is not None:
                assert(row_id in columns)
                self.columns = columns
                # set other column headers
                for idx,column in enumerate(columns):
                    if column is not self.row_id:
                        item = QtGui.QTableWidgetItem(column)
                        item.setBackground(QtGui.QColor(225,225,225))
                        self.insertColumn(idx)
                        self.setHorizontalHeaderItem(idx, item)
                        self.column_dict[column] = idx
            self.setColumnCount(len(self.columns))
        else:
            print("This setting is not supported yet")

        self.horizontalHeader().setStretchLastSection(True)
        # make table non-writable
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(True)
        self.rowcount = 0

    @QtCore.pyqtSlot()
    def updatePosted(self):
        self.scrollToBottom()

    def handle_input(self, pdu):
        #self.setSortingEnabled(False)
        # we expect a pdu
        if not pmt.is_pair(pdu):
            print("Message is not a PDU")
            return
        meta = pmt.car(pdu)
        if not pmt.is_dict(meta):
            print("No meta field present")
            return

        meta_dict = pmt.to_python(meta)
        if(not type(meta_dict) == type({})): 
            return
        # for now, we insist on having the row_id pmt within the meta field
        if meta_dict.has_key(self.row_id):
            # get the current row identifier
            id_value = meta_dict[self.row_id]
            cur_idx = self.rowcount
            create_new_row = id_value not in self.ids.keys()

            if create_new_row:
                #print("Creating new Table Entry with "+str(id_value))
                tab_item = QtGui.QTableWidgetItem(str(id_value))
                tab_item.setData(QtCore.Qt.EditRole, id_value)
                tab_item.setBackground(QtGui.QColor(225,225,225))
                self.setRowCount(self.rowcount + 1)
                self.setItem(self.rowcount, 0, tab_item)
                self.ids[id_value] = tab_item
            else:
                #print("Updating Table Entry " + str(id_value))
                # if row id already exists, get and use the respective row idx
                cur_idx = self.ids[id_value].row()

            for col, idx in self.column_dict.iteritems():
                if meta_dict.has_key(col) and col is not self.row_id:
                    value = meta_dict[col]
                    # for now, we wont allow meta field entrys other than the specified columns
                    tab_item = QtGui.QTableWidgetItem(str(value))
                    tab_item.setData(QtCore.Qt.EditRole, value)
                    self.setItem(cur_idx, idx, tab_item)

            if create_new_row:
                self.rowcount += 1
                self.setRowCount(self.rowcount)
                if self.scroll_to_bottom:
                    self.updateTrigger.emit()
        else:
            print("Meta Field "+self.row_id+" not found.")

        #self.setSortingEnabled(True)

    def work(self, input_items, output_items):
        pass
