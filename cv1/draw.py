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
        self.pol = QPolygonF() # list of QPointFs 
        self.list_of_pols = []
        self.add_vertex =  True
        
    def loadData(self):
        data = gpd.read_file("okresy\Okresy_-_polygony.shp")
        polygony = data.geometry
        list_of_pols = []
        for index, pol in enumerate(polygony):
            g = []
            for i in polygony:
                g.append(i)
            if pol.geom_type == "Polygon":
                x,y = g[index].exterior.coords.xy
            else:
                x,y = g[index].convex_hull.exterior.coords.xy  
            coords = np.dstack((x,y)).tolist()
            for i in coords[0]:
                p = QPointF(i[0],-i[1])
                self.pol.append(p)
            list_of_pols.append(self.pol)
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf
        for p in self.pol:
            if p.x() < xmin:
                xmin = p.x()
            if p.y() < ymin:
                ymin = p.y()
            if p.x() > xmax:
                xmax = p.x()
            if p.y() > ymax:
                ymax = p.y()
        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        for point in self.pol:
            new_x = int((point.x() - xmin) * width/(xmax - xmin))
            new_y = int((point.y() - ymin) * height/(ymax - ymin))
            point.setX(new_x)
            point.setY(new_y)
        self.repaint()
        
        
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
        # for pol in range(len(self.list_of_pols)):
        #     qp.drawPolygon(self.list_of_pols[pol])
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