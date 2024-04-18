from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np
import scipy.linalg as spl
from qpoint3df import *
from line import *

#Processing data
class Algorithms:
    def __init__(self):
        pass
        
    def get2LineAngle(self, p1:QPointF,p2:QPointF,p3:QPointF,p4:QPointF):
        #Compute angle of two lines
        #Get parts of vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()
        
        #Dot product
        dot = ux * vx + uy * vy
        
        #Norms of vectors
        nu = (ux * ux + uy * uy)**(1/2)
        nv = (vx * vx + vy * vy)**(1/2)
        
        #Argument
        arg = dot/(nu*nv)
        
        #In case of extreme values
        arg = max(min(arg, 1), -1)
        
        return acos(arg)    
    
    
    def distance(self, p1:QPointF, p2:QPointF):
        #Compute Euclid distance of two points
        dist = sqrt((p2.x()-p1.x())**2 + (p2.y()-p1.y())**2)
        
        return dist
    
    
    def getPointAndLinePosition(self, p:QPoint3DF, p1:QPoint3DF, p2:QPoint3DF):
        #Analyze point and line position
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        
        vx = p.x() - p1.x()
        vy = p.y() - p1.y()
        
        #Test
        t = ux * vy - uy * vx
        
        #Point in left half-plane
        if t > 0:
            return 1
        
        #Point in right half-plane
        if t < 0:
            return 0
        
        #Point on line
        return -1
    
    
    def getNearestPoint(self, q:QPoint3DF, points:list[QPoint3DF]):
        #Returns nearest point to q
        p_nearest = None
        dist_nearest = inf
        
        #Process all points
        for p in points:
            #Point p different from point q
            if p != q:
            #Calculate distance
                dx = p.x() - q.x()
                dy = p.y() - q.y()
                dist = sqrt(dx**2 + dy**2)
                #Update nearest point
                if dist < dist_nearest:
                    dist_nearest = dist
                    p_nearest = p
                    
        return p_nearest
              
                
    def findDelaunayPoint(self, start:QPoint3DF, end:QPoint3DF, points:list[QPoint3DF]):
        #Find Delaunay point to edge
        p_dt = None
        angle_max = 0
        
        #Process all points
        for p in points:
            #Point p different from points of edge
            if start != p and end != p:
                #Point in left half-plane
                if self.getPointAndLinePosition(p, start, end) == 1:
                    #Compute angle
                    angle = self.get2LineAngle(p, start, p, end)
                    
                    #Update maximum
                    if angle > angle_max:
                        angle_max = angle
                        p_dt = p
        return p_dt
    
    
    def updateAEL(self, e:Edge, ael:list[Edge]):
        #Update active edges list
        e_op = e.changeOrientation()
        #Is edge in ael?
        if e_op in ael:
            #Remove edge
            ael.remove(e_op)
        #Else add edge to ael 
        else:       
            ael.append(e)
    
    def createDT(self, points:list[QPoint3DF]):
        #Create Delaunay triangulation using incermental method
        ael = []
        dt = []
        
        #Sort points by x
        p1 = min(points, key = lambda k: k.x())
        
        #Find nearest point
        p2 = self.getNearestPoint(p1, points)
        
        #Create new edges
        e = Edge(p1, p2)
        e_op = Edge(p2, p1)
        
        #Add egdes to active edges list
        ael.append(e)
        ael.append(e_op)

        #Repeat until ael empty
        while ael:
            #Take first edge
            e1 = ael.pop()
            
            #Change orientation
            e1_op = e1.changeOrientation()
            
            #Find optimal Delaunay point
            p_dt = self.findDelaunayPoint(e1_op.getStart(), e1_op.getEnd(), points)
            
            #Does point exist?
            if p_dt != None:
                #Create remaining edges
                e2 = Edge(e1_op.getEnd(), p_dt)
                e3 = Edge(p_dt, e1_op.getStart())
                
                #Create Delaunay triangle
                dt.append(e1_op)
                dt.append(e2)
                dt.append(e3)
                
                #Update active edges list
                self.updateAEL(e2, ael)
                self.updateAEL(e3, ael)
                
        return dt    