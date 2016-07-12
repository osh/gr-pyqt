#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Such Samples 2, /tmp/such_samples.cfile Woww!!
# Author: Tim O'Shea
# Generated: Tue Jul 12 12:20:31 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy
import pyqt
import sip
import sys


class ss2(gr.top_block, Qt.QWidget):

    def __init__(self, center_freq=0, filename="/tmp/such_samples.cfile", samp_rate=2.4e6):
        gr.top_block.__init__(self, "Such Samples 2, /tmp/such_samples.cfile Woww!!")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Such Samples 2, /tmp/such_samples.cfile Woww!!")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ss2")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq
        self.filename = filename
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.ymin = ymin = -100
        self.ymax = ymax = -40
        self.samp_rate_f = samp_rate_f = samp_rate
        self.center_freq_f = center_freq_f = center_freq

        ##################################################
        # Blocks
        ##################################################
        self._ymin_range = Range(-160, 20, 5, -100, 200)
        self._ymin_win = RangeWidget(self._ymin_range, self.set_ymin, "ymin", "counter_slider", int)
        self.top_grid_layout.addWidget(self._ymin_win, 1,0,1,1)
        self._ymax_range = Range(-160, 20, 5, -40, 200)
        self._ymax_win = RangeWidget(self._ymax_range, self.set_ymax, "ymax", "counter_slider", int)
        self.top_grid_layout.addWidget(self._ymax_win, 1,1,1,1)
        self._samp_rate_f_tool_bar = Qt.QToolBar(self)
        self._samp_rate_f_tool_bar.addWidget(Qt.QLabel("Sample Rate"+": "))
        self._samp_rate_f_line_edit = Qt.QLineEdit(str(self.samp_rate_f))
        self._samp_rate_f_tool_bar.addWidget(self._samp_rate_f_line_edit)
        self._samp_rate_f_line_edit.returnPressed.connect(
        	lambda: self.set_samp_rate_f(eval(str(self._samp_rate_f_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._samp_rate_f_tool_bar, 0,0,1,1)
        self._center_freq_f_tool_bar = Qt.QToolBar(self)
        self._center_freq_f_tool_bar.addWidget(Qt.QLabel("Center Frequency"+": "))
        self._center_freq_f_line_edit = Qt.QLineEdit(str(self.center_freq_f))
        self._center_freq_f_tool_bar.addWidget(self._center_freq_f_line_edit)
        self._center_freq_f_line_edit.returnPressed.connect(
        	lambda: self.set_center_freq_f(eng_notation.str_to_num(str(self._center_freq_f_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._center_freq_f_tool_bar, 0,1,1,1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	center_freq_f, #fc
        	samp_rate_f, #bw
        	"", #name
                0 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)
        
        if not False:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "msg_complex" == "float" or "msg_complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(ymin, ymax)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 2,0,2,2)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate_f, #samp_rate
        	"", #name
        	0 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 2,2,1,1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	center_freq_f, #fc
        	samp_rate_f, #bw
        	"", #name
        	0 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(ymin, ymax)
        self.qtgui_freq_sink_x_0.set_y_label("Relative Gain", "dB")
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "msg_complex" == "float" or "msg_complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 3,2,1,1)
        self.pyqt_set_title_0 = pyqt.set_title(parent=self, prefix="Such Samples: ")
        self.pyqt_select_input_1 = pyqt.select_input(opt=['c_int16', 'c_uint16', 'c_int32', 'c_uint32', 'complex64', 'float32', 'c_<i2', 'c_>i2', 'c_<i4', 'c_>i4'])
        self._pyqt_select_input_1_win = self.pyqt_select_input_1;
        self.top_grid_layout.addWidget(self._pyqt_select_input_1_win, 1,2,1,1)
        self.pyqt_range_input_0 = pyqt.range_input()
        self._pyqt_range_input_0_win = self.pyqt_range_input_0;
        self.top_grid_layout.addWidget(self._pyqt_range_input_0_win, 0,2,1,2)
        self.pyqt_open_0 = pyqt.file_open(label="Open")
        self._pyqt_open_0_win = self.pyqt_open_0;
        self.top_layout.addWidget(self._pyqt_open_0_win)
        self.pyqt_file_message_souce_0 = pyqt.file_message_source(filename, "complex64")
        self.pyqt_file_message_sink_0 = pyqt.file_message_sink(filename+".excerpt", "complex64", "Save Segment")
        self._pyqt_file_message_sink_0_win = self.pyqt_file_message_sink_0;
        self.top_layout.addWidget(self._pyqt_file_message_sink_0_win)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pyqt_file_message_souce_0, 'pdus'), (self.pyqt_file_message_sink_0, 'pdus'))    
        self.msg_connect((self.pyqt_file_message_souce_0, 'file_range'), (self.pyqt_range_input_0, 'file_range'))    
        self.msg_connect((self.pyqt_file_message_souce_0, 'pdus'), (self.qtgui_freq_sink_x_0, 'in'))    
        self.msg_connect((self.pyqt_file_message_souce_0, 'pdus'), (self.qtgui_time_sink_x_0, 'in'))    
        self.msg_connect((self.pyqt_file_message_souce_0, 'pdus'), (self.qtgui_waterfall_sink_x_0, 'in'))    
        self.msg_connect((self.pyqt_open_0, 'filename'), (self.blocks_message_debug_0, 'print'))    
        self.msg_connect((self.pyqt_open_0, 'filename'), (self.pyqt_file_message_souce_0, 'file_open'))    
        self.msg_connect((self.pyqt_open_0, 'filename'), (self.pyqt_set_title_0, 'name'))    
        self.msg_connect((self.pyqt_range_input_0, 'range'), (self.pyqt_file_message_souce_0, 'range'))    
        self.msg_connect((self.pyqt_select_input_1, 'pdus'), (self.pyqt_file_message_souce_0, 'file_type'))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ss2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_center_freq_f(self.center_freq)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_f(self.samp_rate)

    def get_ymin(self):
        return self.ymin

    def set_ymin(self, ymin):
        self.ymin = ymin
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.ymin, self.ymax)
        self.qtgui_freq_sink_x_0.set_y_axis(self.ymin, self.ymax)

    def get_ymax(self):
        return self.ymax

    def set_ymax(self, ymax):
        self.ymax = ymax
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.ymin, self.ymax)
        self.qtgui_freq_sink_x_0.set_y_axis(self.ymin, self.ymax)

    def get_samp_rate_f(self):
        return self.samp_rate_f

    def set_samp_rate_f(self, samp_rate_f):
        self.samp_rate_f = samp_rate_f
        Qt.QMetaObject.invokeMethod(self._samp_rate_f_line_edit, "setText", Qt.Q_ARG("QString", repr(self.samp_rate_f)))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq_f, self.samp_rate_f)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate_f)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq_f, self.samp_rate_f)

    def get_center_freq_f(self):
        return self.center_freq_f

    def set_center_freq_f(self, center_freq_f):
        self.center_freq_f = center_freq_f
        Qt.QMetaObject.invokeMethod(self._center_freq_f_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.center_freq_f)))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq_f, self.samp_rate_f)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq_f, self.samp_rate_f)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--center-freq", dest="center_freq", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set center_freq [default=%default]")
    parser.add_option(
        "", "--filename", dest="filename", type="string", default="/tmp/such_samples.cfile",
        help="Set filename [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(2.4e6),
        help="Set samp_rate [default=%default]")
    return parser


def main(top_block_cls=ss2, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(center_freq=options.center_freq, filename=options.filename, samp_rate=options.samp_rate)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
