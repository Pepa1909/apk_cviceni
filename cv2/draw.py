from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = QPolygonF()
        self.ch = QPolygonF() # convex hull
        self.mbr = QPolygonF() # minimum bounding rectangle
        
    def mousePressEvent(self, e: QMouseEvent):
        # get coordinates
        x = e.position().x()
        y = e.position().y()
        
        # add new vertex
        # create temporary point
        p = QPointF(x, y)
        
        # add point to polygon
        self.building.append(p)
        
        # repaint screen
        self.repaint()
        
    def paintEvent(self, e: QPaintEvent):
        # draw situation
        # create gprahic object
        qp = QPainter(self)
        
        # start drawing
        qp.begin(self)
        
        # set graphical attributes building
        qp.setPen(Qt.GlobalColor.cyan)
        qp.setBrush(Qt.GlobalColor.magenta)
        
        # draw building
        qp.drawPolygon(self.building)
        
        # set graphical attributes CH
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.red)
        
        # draw CH
        
        # set graphical attributes MBR
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)
        
        # draw MBR
        qp.drawPolygon(self.mbr)
        
        # end drawing
        qp.end()
    
    def getBuilding(self):
        # return analyzed polygon
        return self.building
    
    def setMBR(self, mbr):
        # set result
        self.mbr = mbr
        
    def clearData(self):
        # clear building
        self.building.clear()
        
        # clear CH
        self.ch.clear()
        
        # clear MBR
        self.mbr.clear()
        
        # repaint screen
        self.repaint()