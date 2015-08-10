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
import pylab

from PyQt4 import Qt, QtCore, QtGui
import PyQt4.Qwt5 as Qwt
#from PyQt4.Qwt5.anynumpy import *
from numpy import ravel, asarray
from numpy import uint8 as UInt8
import pmt,threading

def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    if ((hasattr(data, 'dtype') and data.dtype.char == UInt8)
        or (hasattr(data, 'typecode') and data.typecode == UInt8)
        ):
        return data
    high = high - low
    if cmin is None:
        cmin = min(ravel(data))
    if cmax is None:
        cmax = max(ravel(data))
    scale = high * 1.0 / (cmax-cmin or 1)
    bytedata = ((data*1.0-cmin)*scale + 0.4999).astype(UInt8)
    return bytedata + asarray(low).astype(UInt8)

class PlotImage(Qwt.QwtPlotItem):

    def __init__(self, title = Qwt.QwtText(), mincol = 50, minrow = 50):
        Qwt.QwtPlotItem.__init__(self)
        if not isinstance(title, Qwt.QwtText):
            self.title = Qwt.QwtText(str(title))
        else:
            self.title = title
        self.setItemAttribute(Qwt.QwtPlotItem.Legend);
        self.xyzs = None
    
        self.X = numpy.zeros([minrow, mincol])


    def setData(self, xyzs, xRange = None, yRange = None):
        self.xyzs = xyzs
        shape = xyzs.shape
        if not xRange:
            xRange = (0, shape[0])
        if not yRange:
            yRange = (0, shape[1])

        self.xMap = Qwt.QwtScaleMap(0, xyzs.shape[0], *xRange)
        self.plot().setAxisScale(Qwt.QwtPlot.xBottom, *xRange)
        self.yMap = Qwt.QwtScaleMap(0, xyzs.shape[1], *yRange)
        self.plot().setAxisScale(Qwt.QwtPlot.yLeft, *yRange)

        self.image = Qwt.toQImage(bytescale(self.xyzs)).mirrored(False, True)
        self.genColor();

    def genColor(self):   
        points = [(255,0,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255)]
        for i in range(0, 256):
            p0 = int(numpy.floor((i/256.0)/len(points)))
            p1 = int(numpy.ceil((i/256.0)/len(points)))
            rgb = map(lambda x: x[0]*max(0,(i-p0)) + x[1]*max(0,(i-p1)), zip(points[p0], points[p1]))
            self.image.setColor(i, QtGui.qRgb(rgb[0], rgb[1], rgb[2]))

    # setData()    

    def updateLegend(self, legend):
        Qwt.QwtPlotItem.updateLegend(self, legend)
        legend.find(self).setText(self.title)

    # updateLegend()

    def draw(self, painter, xMap, yMap, rect):
        """Paint image zoomed to xMap, yMap
        Calculate (x1, y1, x2, y2) so that it contains at least 1 pixel,
        and copy the visible region to scale it to the canvas.
        """
        assert(isinstance(self.plot(), Qwt.QwtPlot))
        
        # calculate y1, y2
        # the scanline order (index y) is inverted with respect to the y-axis
        y1 = y2 = self.image.height()
        y1 *= (self.yMap.s2() - yMap.s2())
        y1 /= (self.yMap.s2() - self.yMap.s1())
        y1 = max(0, int(y1-0.5))
        y2 *= (self.yMap.s2() - yMap.s1())
        y2 /= (self.yMap.s2() - self.yMap.s1())
        y2 = min(self.image.height(), int(y2+0.5))
        # calculate x1, x2 -- the pixel order (index x) is normal
        x1 = x2 = self.image.width()
        x1 *= (xMap.s1() - self.xMap.s1())
        x1 /= (self.xMap.s2() - self.xMap.s1())
        x1 = max(0, int(x1-0.5))
        x2 *= (xMap.s2() - self.xMap.s1())
        x2 /= (self.xMap.s2() - self.xMap.s1())
        x2 = min(self.image.width(), int(x2+0.5))
        # copy
        image = self.image.copy(x1, y1, x2-x1, y2-y1)
        # zoom
        image = image.scaled(xMap.p2()-xMap.p1()+1, yMap.p1()-yMap.p2()+1)
        # draw
        painter.drawImage(xMap.p1(), yMap.p2(), image)
    
    def add_row(self, x):

        # frow our width if needed
        if( x.shape[0] > self.X.shape[1]):
            self.X.resize( (self.X.shape[0], x.shape[0]), refcheck = False )
 
        # shift existing rows up, add new row
        self.X[1:,:] = self.X[0:-1,:]
        self.X[0,:] = 0;
        self.X[0,0:x.shape[0]] = x
        self.setData(self.X)

class raster_plot(gr.sync_block, Qwt.QwtPlot):
    __pyqtSignals__ = ("updatePlot(int)")

    def __init__(self, blkname="pyqt_raster", label="", *args):
        gr.sync_block.__init__(self,blkname,[],[])
        Qwt.QwtPlot.__init__(self, *args)
        self.enabled = True

        # set up message port
        self.message_port_register_in(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handler);
        
        # QwtPlot set up
        self.setMinimumWidth(100)
        self.setMinimumHeight(100)

        self._lock = threading.Lock();

        # set up label if desired
        if not label == "":
            ttl = Qwt.QwtText(label)
            ttl.setFont(Qt.QFont("Helvetica",10))
            self.setTitle(ttl)

        # wedge everything as close as possible
        self.plotLayout().setMargin(0)
        self.plotLayout().setCanvasMargin(0)
        self.plotLayout().setSpacing(0)

        # set up background etc
        self.setCanvasBackground(Qt.Qt.black)
        self.alignScales()

        # set up image raster
        dim = (100,100)
        self.__data = PlotImage('Image', dim[0], dim[1])
        self.__data.attach(self)
        self.__data.setData( numpy.random.normal(0,1e-9,dim) )
        self.replot()

        # connect the plot callback signal
        QtCore.QObject.connect(self,
                       QtCore.SIGNAL("updatePlot(int)"),
                       self.do_plot)

        # set up zoomer
        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
                                        Qwt.QwtPlot.yLeft,
                                        Qwt.QwtPicker.DragSelection,
                                        Qwt.QwtPicker.AlwaysOff,
                                        self.canvas())
        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.black))

        # Set up menu actions
        actions = [("Start/Stop", self.toggle_enabled),
                  ]
        self.actions = [];
        for a in actions:
            action = QtGui.QAction(a[0], self)
            action.triggered.connect(a[1])
            self.actions.append(action)

    # pop up a context menu
    def triggerMenu(self, pos):
        menu = QtGui.QMenu(self)
        for a in self.actions:
            menu.addAction(a)
        menu.exec_(pos)

    # override default mousePressEvent
    def mousePressEvent(self, ev):
        # context menu on middle click
        if(ev.buttons() == Qt.Qt.MiddleButton):
            self.triggerMenu(ev.globalPos())

    def toggle_enabled(self):
        self.enabled = not self.enabled
 
    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(
                    Qwt.QwtAbstractScaleDraw.Backbone, False)

    def do_plot(self, a):
        if len(self.zoomer.zoomStack()) == 1:
            self.setAxisAutoScale(Qwt.QwtPlot.xBottom)
            self.setAxisAutoScale(Qwt.QwtPlot.yLeft)
            self.zoomer.setZoomBase()
        self.replot();

    def work(self, input_items, output_items):
        pass

    def handler(self, msg):
        if(self.enabled):
            self._lock.acquire();
    
            # get input msg
            meta = pmt.car(msg);
            samples = pmt.cdr(msg);
            x = pmt.to_python(pmt.cdr(msg))*1.0
    
            # add to raster
            self.__data.add_row(x)
    
            # update plot
            self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)
            
            self._lock.release();

class raster_test_top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        import pyqt
        from gnuradio import blocks
        self.strobe = blocks.message_strobe( 
                pmt.cons(
                    pmt.PMT_NIL,
                    pmt.to_pmt( numpy.random.normal( 0, 1, 256 ) )
                ), 
                500 )
                
        self.raster = raster_plot("")
        self._raster_win = self.raster;
        self.top_layout.addWidget(self._raster_win)
        self.msg_connect( self.strobe, "strobe", self.raster, "pdus" )


if __name__ == '__main__':
    from optparse import OptionParser
    from gnuradio import eng_notation
    from gnuradio.eng_option import eng_option
    from distutils.version import StrictVersion
    import sys
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = raster_test_top_block()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets


