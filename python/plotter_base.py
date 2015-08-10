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
import numpy
from gnuradio import gr;
import pylab

from PyQt4 import Qt, QtCore, QtGui
import PyQt4.Qwt5 as Qwt
#from PyQt4.Qwt5.anynumpy import *
import pmt

class plotter_base(gr.sync_block, Qwt.QwtPlot):
    __pyqtSignals__ = ("updatePlot(int)")

    def __init__(self, blkname="pyqt_plotter", label="", *args):
        gr.sync_block.__init__(self,blkname,[],[])
        Qwt.QwtPlot.__init__(self, *args)

        self.enabled = True
        self.setMinimumWidth(100)
        self.setMinimumHeight(100)

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

        # curve storage
        self.curves = [];
        self.curve_data = [];

        # connect the plot callback signal
        QtCore.QObject.connect(self,
                       QtCore.SIGNAL("updatePlot(int)"),
                       self.do_plot)
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
                   ("Toggle Grid", self.toggle_grid),
                   ("Toggle Axes", self.toggle_axes),
                   ("Clear Markers", self.clear_markers)
                  ]
        self.actions = [];
        for a in actions:
            action = QtGui.QAction(a[0], self)
            action.triggered.connect(a[1])
            self.actions.append(action)

        # set up some other stuff ...
        self.grid = None
        self.toggle_axes()
#        self.toggle_grid()
        self.markers = []

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
    
        # add a marker on shift left click
        if((ev.buttons() == Qt.Qt.LeftButton) and (ev.modifiers() == Qt.Qt.ShiftModifier)):

            m = Qwt.QwtPlotMarker()
            (x,y) = (self.invTransform(Qwt.QwtPlot.xBottom, ev.x()),
               self.invTransform(Qwt.QwtPlot.yLeft, ev.y()))
            m.setValue(x,y)

            lbl = Qwt.QwtText("test")
            lbl.setText(
            'x = %+.6g, y = %.6g'
            % (self.invTransform(Qwt.QwtPlot.xBottom, ev.x()),
               self.invTransform(Qwt.QwtPlot.yLeft, ev.y())))
            lbl.setColor(Qt.Qt.cyan)

            m.setLabel(lbl)
            m.attach(self)
            self.markers.append(m)
            self.trigger_update()

    def toggle_enabled(self):
        self.enabled = not self.enabled

    # turn curve[0] line off (dots only)
    def line_off(self, size=2):
        self.curves[0].setStyle(Qwt.QwtPlotCurve.NoCurve);
        self.curves[0].setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.XCross,
                                  Qt.QBrush(),
                                  Qt.QPen(Qt.Qt.green),
                                  Qt.QSize(size, size)))

    # toggle grid status
    def toggle_grid(self):
        print "toggle grid"
        if self.grid == None:
            self.grid = Qwt.QwtPlotGrid()
            self.grid.enableXMin(True)
            self.grid.setMajPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.DotLine))
            self.grid.setMinPen(Qt.QPen(Qt.Qt.darkGray, 0 , Qt.Qt.DotLine))
            self.grid.attach(self)
        else:
            self.grid.detach()
            self.grid = None
        self.trigger_update()
 
    # remove all markers
    def clear_markers(self):
        for m in self.markers:
            m.detach()
        self.markers = []
        self.trigger_update()

    def trigger_update(self):
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)   

    # toggle axes status
    def toggle_axes(self):
        ax_en = not self.axisEnabled(Qwt.QwtPlot.yLeft)
        self.enableAxis(Qwt.QwtPlot.yLeft,ax_en)
        self.enableAxis(Qwt.QwtPlot.xBottom,ax_en)
    
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
        if not self.enabled:    
            return
        # set curve data for known curves
        for cd in self.curve_data:
            for c in cd:
                if(numpy.isnan(numpy.sum(c))): 
                    print "WARNING: gr-pyqt discarding NaN data"
                    return
        
        nchan = min(len(self.curves),len(self.curve_data))
        map(lambda x: self.curves[x].setData(self.curve_data[x][0], self.curve_data[x][1]), range(0,nchan));

        if len(self.zoomer.zoomStack()) == 1:
            self.setAxisAutoScale(Qwt.QwtPlot.xBottom)
            self.setAxisAutoScale(Qwt.QwtPlot.yLeft)
            self.zoomer.setZoomBase()
        self.replot();

    def work(self, input_items, output_items):
        pass




