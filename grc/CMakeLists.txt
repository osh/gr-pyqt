# Copyright 2011 Free Software Foundation, Inc.
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

install(FILES
    time_plot.xml
    time_hist.xml
    value_plot.xml
    value_hist.xml
    const_plot.xml
    ctime_plot.xml
    cpsd_plot.xml
    cpower_plot.xml
    pdu_meta_extract.xml
    text_input.xml
    text_output.xml
    meta_text_output.xml
    DESTINATION share/gnuradio/grc/blocks
)
