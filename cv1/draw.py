from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = QPointF(-100, -100)
        self.pol = QPolygonF() # list of QPointFs 
        self.add_vertex =  True
        
    def mousePressEvent(self, e: QMouseEvent):
        # get coordinates
        x = e.position().x()
        y = e.position().y()
        
        # add new vertex
        if self.add_vertex:
            # create temporary point
            p = QPointF(x, y)
            
            # add point to polygon
            self.pol.append(p)
            
        # move q    
        else:
            self.q.setX(x)
            self.q.setY(y)
        
        # repaint screen
        self.repaint()
        
    def paintEvent(self, e: QPaintEvent):
        # draw situation
        # create gprahic object
        qp = QPainter(self)
        
        # start drawing
        qp.begin(self)
        
        # set graphical attributes
        qp.setPen(Qt.GlobalColor.cyan)
        qp.setBrush(Qt.GlobalColor.magenta)
        
        # draw polygon
        qp.drawPolygon(self.pol)
        
        # set graphical attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.red)
        
        # draw point
        r = 5
        qp.drawEllipse(int(self.q.x() - r),int(self.q.y() - r), 2 * r, 2 * r)
        
        # end drawing
        qp.end()
        
    def switchDrawing(self):
        # change drawing - point or polygon
        self.add_vertex = not(self.add_vertex)
    
    def getQ(self):
        # return analyzed point
        return self.q
    
    def getPol(self):
        # return analyzed polygon
        return self.pol
    
    def clearData(self):
        # clear polygon
        self.pol.clear()
        
        # shift point
        self.q.setX(-100)
        self.q.setY(-100)
        
        self.repaint()