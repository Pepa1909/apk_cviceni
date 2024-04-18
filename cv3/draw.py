from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import geopandas as gpd
import numpy as np
from math import inf
from line import *
from qpoint3df import *
import algorithms

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = []
        self.dt = []
        
    def mousePressEvent(self, e: QMouseEvent):
        # get coordinates
        x = e.position().x()
        y = e.position().y()
        
        p = QPointF(x, y)
        
        self.points.append(p)
        
        # repaint screen
        self.repaint()
        
    def paintEvent(self, e: QPaintEvent):
        # draw situation
        # create gprahic object
        qp = QPainter(self)
        
        # start drawing
        qp.begin(self)
        
        # set graphical attributes        
        qp.setBrush(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw points
        r = 5
        for p in self.points:
            qp.drawEllipse(int(p.x() - r),int(p.y() - r), 2 * r, 2 * r)
                       
        # set graphical attributes
        qp.setPen(Qt.GlobalColor.green)
        qp.setBrush(Qt.GlobalColor.transparent)
        
        #Draw edges
        for e in self.dt:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))
        
        #Draw countour lines
        
        #Draw slope
        
        #Draw aspect
        
        
        # end drawing
        qp.end()
    
    def getPoints(self):
        #Return points
        return self.points
       
    def clearData(self):
        # clear polygon
        self.points.clear()
        self.dt.clear()
        
        self.repaint()
        
    def setDT(self, dt:list[Edge]):
        self.dt = dt