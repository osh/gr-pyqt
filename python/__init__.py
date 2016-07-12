#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio PYQT module. Place your Python package
description here (python/__init__.py).
'''

# ----------------------------------------------------------------
# Temporary workaround for ticket:181 (swig+python problem)
import sys
_RTLD_GLOBAL = 0
try:
    from dl import RTLD_GLOBAL as _RTLD_GLOBAL
except ImportError:
    try:
	from DLFCN import RTLD_GLOBAL as _RTLD_GLOBAL
    except ImportError:
	pass

if _RTLD_GLOBAL != 0:
    _dlopenflags = sys.getdlopenflags()
    sys.setdlopenflags(_dlopenflags|_RTLD_GLOBAL)
# ----------------------------------------------------------------


# import swig generated symbols into the pyqt namespace
#from pyqt_swig import *

# import any pure python here
#

from pdu_lambda import *;
from stream_lambda import *;
from plotter_base import *;
from const_plot import *;
from ctime_plot import *;
from raster_plot import *;
from cpsd_plot import *;
from time_plot import *;
from time_hist import *;
from value_plot import *;
from value_hist import *;
from cpower_plot import *;
from pdu_meta_extract import *;
from text_input import *;
from select_input import *;
from variable_text_input import *;
from range_input import *;
from text_output import *;
from meta_text_output import *;
from skip_head import *
from head import *
from trim_tail import *
from file_message_source import *
from file_message_sink import *
from file_open import *
from set_title import *
from table import *
from dict_ui_source import *

# ----------------------------------------------------------------
# Tail of workaround
if _RTLD_GLOBAL != 0:
    sys.setdlopenflags(_dlopenflags)      # Restore original flags
# ----------------------------------------------------------------
