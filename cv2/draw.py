from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *
from math import inf
import numpy as np

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building_list = []
        self.mbr_list = []
        
    def paintEvent(self, e: QPaintEvent):
        #Draw situation
        #Create graphic object
        qp = QPainter(self)
        
        #Start drawing
        qp.begin(self)
        
        #Set graphical attributes building
        qp.setPen(Qt.GlobalColor.cyan)
        qp.setBrush(Qt.GlobalColor.magenta)
        
        #Iterate over all buildings
        for pol in self.building_list:       
            qp.setBrush(Qt.GlobalColor.yellow)
            qp.drawPolygon(pol)
        
        #Set graphical attributes of MAER
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)
        
        #Draw MAERs
        for mbr in self.mbr_list:
            qp.drawPolygon(mbr)
        
        #End drawing
        qp.end()
    
    def getBuilding(self):
        #Return analyzed polygon list
        return self.building_list
        
    def clearAll(self):
        #Clear results and buildings
        self.building_list = []
        self.mbr_list = []
        
        #Repaint screen
        self.repaint()
    
    def clearResults(self):
        #Clear results
        self.mbr_list = []
        
        #Reapint screen
        self.repaint()
        
    def findBoundingPoints(self, p:QPointF, xmin, ymin, xmax, ymax):
        #Returns minimum and maximum coordinates of bounding box around input polygons
        if p.x() < xmin:
            xmin = p.x()
        if p.y() < ymin:
            ymin = p.y()
        if p.x() > xmax:
            xmax = p.x()
        if p.y() > ymax:
            ymax = p.y()
            
        return xmin, ymin, xmax, ymax
    
    def resizePolygons(self, pol_list, xmin, ymin, xmax, ymax):
        #Resizes input data to fit to display
        
        canvas_height = self.frameGeometry().height()
        canvas_width = self.frameGeometry().width()
        
        #Iterate over each coordinate for repositioning
        for polygon in pol_list:
            for point in polygon:
                new_x = int((point.x() - xmin) * canvas_width/(xmax - xmin))
                new_y = int((point.y() - ymin) * canvas_height/(ymax - ymin))
                
                #Reposition coordinates accordingly
                point.setX(new_x)
                point.setY(new_y)
    
    def loadData(self, data):
        #Loads input shapefile
        polygony = data.geometry
        
        #Initialize min and max coordinates to compute bounding box of file
        xmin = inf
        ymin = inf
        xmax = -inf
        ymax = -inf
        
        #Iterate over all polygons
        for polyg in polygony:
            
            #Create empty polygon
            pol = QPolygonF()
            x,y = polyg.exterior.coords.xy

            #Create a list of points
            coords = np.dstack((x,y)).tolist()
            
            #Iterate over every point and add it to polygon
            for i in coords[0]:
                p = QPointF(i[0],-i[1])
                pol.append(p)
                
                #Find bounding points of polygon
                xmin, ymin, xmax, ymax = self.findBoundingPoints(p, xmin, ymin, xmax, ymax)
            
            #Add polygon to list of polygons and set status to 0
            self.building_list.append(pol)
            
            
        #Resize all polygons and min-max boxes according to the canvas size
        self.resizePolygons(self.building_list, xmin, ymin, xmax, ymax)
        self.repaint()