from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import geopandas as gpd
import numpy as np
from math import *
from line import *
from qpoint3df import *
import algorithms
from random import *
from triangle import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = []
        self.dt = []
        self.contours = []
        self.dtm_slope = []
        self.dtm_aspect = []
        self.viewDT = True
        self.viewContours = True
        self.viewSlope = True
        self.viewAspect = True
        
    def mousePressEvent(self, e: QMouseEvent):
        # get coordinates
        x = e.position().x()
        y = e.position().y()
        
        #Set height 
        zmin = 150
        zmax = 400
        z = random() * (zmax - zmin) + zmin
        
        p = QPoint3DF(x, y, z)
        
        self.points.append(p)
        
        # repaint screen
        self.repaint()
        
    def paintEvent(self, e: QPaintEvent):
        # draw situation
        # create gprahic object
        qp = QPainter(self)
        
        # start drawing
        qp.begin(self)
        
        if self.viewSlope:
        # set graphical attributes
            qp.setPen(Qt.GlobalColor.gray)
    
        #Draw slope
        
            for t in self.dtm_slope:
                slope = t.getSlope()
                
                #Convert slope to color
                mju = 2*255/pi
                col = int(255 - mju*slope)
                color = QColor(col, col, col)
                qp.setBrush(color)
                
                #Draw triangle
                qp.drawPolygon(t.getVertices())
        
        
        if self.viewAspect:
        # set graphical attributes
            qp.setPen(Qt.GlobalColor.gray)

        #Draw aspect
        
            for t in self.dtm_aspect:
                aspect = t.getAspect()
                col = int((aspect+pi)/(2*pi) * 359)%360
                print(col)
                color = QColor.fromHsv(col, 255,255)
                qp.setBrush(color)
                
                #Draw triangle
                qp.drawPolygon(t.getVertices())
                       
        if self.viewDT:
            # set graphical attributes
            qp.setPen(Qt.GlobalColor.green)
            qp.setBrush(Qt.GlobalColor.transparent)
            
            #Draw triangulation
            for e in self.dt:
                qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))
        
        if self.viewContours:
            # set graphical attributes        
            qp.setPen(Qt.GlobalColor.red)
            qp.setBrush(Qt.GlobalColor.yellow)    
            
            #Draw countour lines
            for c in self.contours:
                qp.drawLine(int(c.getStart().x()), int(c.getStart().y()), int(c.getEnd().x()), int(c.getEnd().y()))
            
        # set graphical attributes        
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw points
        r = 5
        for p in self.points:
            qp.drawEllipse(int(p.x() - r),int(p.y() - r), 2 * r, 2 * r)
        
        # end drawing
        qp.end()
    
    def getPoints(self):
        #Return points
        return self.points
    
    def getDT(self):
        #Return DT
        return self.dt
       
    def clearResults(self):
        # clear polygon
        self.dt.clear()
        self.dtm_aspect.clear()
        self.dtm_slope.clear()
        self.contours.clear()
        
        self.repaint()
    
    def clearAll(self):
        # clear polygon
        self.points.clear()
        self.dt.clear()
        self.dtm_aspect.clear()
        self.dtm_slope.clear()
        self.contours.clear()
        
        self.repaint()
            
    
    def setDT(self, dt:list[Edge]):
        #Set DT
        self.dt = dt
        
    def setContours(self, contours):
        #Set contours
        self.contours = contours
        
    def setDTMSlope(self, dtm_slope:list[Triangle]):
        #Set slope
        self.dtm_slope = dtm_slope
        
    def setDTMAspect(self, dtm_aspect:list[Triangle]):
        #Set aspect
        self.dtm_aspect = dtm_aspect
    
    def setViewDT(self, viewDT):
        self.viewDT = viewDT
    
    def setViewSlope(self, viewSlope):
        self.viewSlope = viewSlope
    
    def setViewAspect(self, viewAspect):
        self.viewAspect = viewAspect
    
    def setViewContours(self, viewContours):
        self.viewContours = viewContours