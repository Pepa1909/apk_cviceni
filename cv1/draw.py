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
        self.polyg_status = []
        self.minmaxbox_list = []
        
    def loadData(self, data):
        polygony = data.geometry
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf
        for index, polyg in enumerate(polygony):
            pol = QPolygonF()
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
                xmin, ymin, xmax, ymax = self.bounding(p, xmin, ymin, xmax, ymax)
            self.list_of_pols.append(pol)
            self.polyg_status.append(0)
            minmaxbox = self.minMaxBox(pol)
            self.minmaxbox_list.append(minmaxbox)
        self.resize(xmin, ymin, xmax, ymax, self.list_of_pols)
        self.resize(xmin, ymin, xmax, ymax, self.minmaxbox_list)
        self.repaint()
       
    def minMaxBox(self, pol: QPolygonF):
        
        px_min = min(pol, key = lambda k: k.x())
        px_max = max(pol, key = lambda k: k.x())
        
        py_min = min(pol, key = lambda k: k.y())
        py_max = max(pol, key = lambda k: k.y())
        
        # new points with only min and max coords
        v1 = QPointF(px_min.x(), py_min.y())
        v2 = QPointF(px_max.x(), py_min.y())
        v3 = QPointF(px_max.x(), py_max.y())
        v4 = QPointF(px_min.x(), py_max.y())
        
        # create min_max box
        box = QPolygonF([v1,v2,v3,v4])
        
        return box
    
    def resize(self, xmin, ymin, xmax, ymax, list_of_pols):
        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        for pol in list_of_pols:
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
    
    def getminmaxes(self):
        return self.minmaxbox_list
    
    def getPol(self):
        # return analyzed polygon
        return self.list_of_pols
       
    def clearData(self):
        # clear polygon
        self.list_of_pols.clear()
        self.minmaxbox_list.clear()
        
        # shift point
        self.q.setX(-100)
        self.q.setY(-100)
        
        self.repaint()