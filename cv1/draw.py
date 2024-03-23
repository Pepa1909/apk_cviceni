from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import geopandas as gpd
import numpy as np
from math import inf

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = QPointF(-100, -100)
        self.list_of_pols = []
        self.list_of_polmms = []
        self.polyg_status = []
        self.add_vertex =  True
        
    def loadData(self, data):
        polygony = data.geometry
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf
        for index, polyg in enumerate(polygony):
            x_pol_min = inf
            y_pol_min = inf
            x_pol_max = -inf
            y_pol_max = -inf
            pol = QPolygonF()
            pol_mm = QPolygonF()
            g = []
            for i in polygony:
                g.append(i)
            if polyg.geom_type == "Polygon":
                x,y = g[index].exterior.coords.xy
            else:
                x,y = g[index].convex_hull.exterior.coords.xy  
            coords = np.dstack((x,y)).tolist()
            for i in coords[0]:
                p = QPointF(i[0],-i[1])
                pol.append(p)
                x_pol_min, y_pol_min, x_pol_max, y_pol_max = self.bounding(p, x_pol_min, y_pol_min, x_pol_max, y_pol_max)
                xmin, ymin, xmax, ymax = self.bounding(p, xmin, ymin, xmax, ymax)
            self.list_of_pols.append(pol)
            self.list_of_polmms.append(pol_mm)
            self.polyg_status.append(0)
        self.resize(xmin, ymin, xmax, ymax)
        self.resize(x_pol_min, y_pol_min, x_pol_max, y_pol_max)
        pol_mm = QPolygonF([QPointF(x_pol_min,y_pol_min), QPointF(x_pol_min, y_pol_max), QPointF(y_pol_max,y_pol_max), QPointF(x_pol_max,y_pol_min)])
        self.repaint()
       
    def resize(self, xmin, ymin, xmax, ymax):
        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        for pol in self.list_of_pols:
            for p in pol:
                new_x = int((p.x() - xmin) * width/(xmax - xmin))
                new_y = int((p.y() - ymin) * height/(ymax - ymin))
                p.setX(new_x)
                p.setY(new_y)
                
    def bounding(self, p, xmin, ymin, xmax, ymax):
            if p.x() < xmin:
                xmin = p.x()
            if p.y() < ymin:
                ymin = p.y()
            if p.x() > xmax:
                xmax = p.x()
            if p.y() > ymax:
                ymax = p.y()
            return xmin, ymin, xmax, ymax
            
        
        
    def mousePressEvent(self, e: QMouseEvent):
        # get coordinates
        x = e.position().x()
        y = e.position().y()
        
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
                
        # draw polygon
        for i, pol in enumerate(self.list_of_pols):
            if self.polyg_status[i] == True:
                qp.setBrush(Qt.GlobalColor.yellow)
            else:
                qp.setBrush(Qt.GlobalColor.magenta)
            qp.drawPolygon(pol)
        
        # set graphical attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.red)
        
        # draw point
        r = 5
        qp.drawEllipse(int(self.q.x() - r),int(self.q.y() - r), 2 * r, 2 * r)
        
        # end drawing
        qp.end()
    
    def getQ(self):
        # return analyzed point
        return self.q
    
    def getPol(self):
        # return analyzed polygon
        return self.list_of_pols
    
    def clearData(self):
        # clear polygon
        self.list_of_pols.clear()
        
        # shift point
        self.q.setX(-100)
        self.q.setY(-100)
        
        self.repaint()