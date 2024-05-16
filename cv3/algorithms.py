from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np
import scipy.linalg as spl
from qpoint3df import *
from line import *
from triangle import *

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
    
    def getContourPoint(self, p1:QPoint3DF, p2:QPoint3DF, z:float):
        #Intersection of triangle and horizontal plane
        xb = ((p2.x() - p1.x())/(p2.getZ() - p1.getZ())) * (z - p1.getZ()) + p1.x()
        yb = ((p2.y() - p1.y())/(p2.getZ() - p1.getZ())) * (z - p1.getZ()) + p1.y()
        
        return QPoint3DF(xb, yb, z)
    
    def createContourLines(self, dt, zmin, zmax, dz):
        #Create contour lines within interval and with given step
        contours:list[Edge] = []
        
        #Process by triangles
        for i in range(0, len(dt), 3):
            #Vertices of triangle
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()
            
            #Get z coordinates
            z1 = p1.getZ()
            z2 = p2.getZ()
            z3 = p3.getZ()
            
            #Create all countours
            for z in np.arange(zmin, zmax, dz):
                #Compute height differences of edges
                dz1 = z - z1
                dz2 = z - z2
                dz3 = z - z3
                
                #Skip coplanar triangle
                if dz1 == 0 and dz2 == 0 and dz3 == 0:
                    continue
                
                #Edge p1p2 colinear
                elif dz1 == 0 and dz2 == 0:
                    contours.append(dt[i])
                
                #Edge p2p3 colinear
                elif dz2 == 0 and dz3 == 0:
                    contours.append(dt[i+1])
                        
                #Edge p1p3 colinear
                elif dz1 == 0 and dz3 == 0:
                    contours.append(dt[i+2])
                    
                #Edges p1p2 and p2p3 intersecting with plane        
                elif dz1 * dz2 <= 0 and dz2 * dz3 <= 0:         
                    #Compute intersetions
                    a = self.getContourPoint(p1, p2, z)
                    b = self.getContourPoint(p2, p3, z)
                    
                    #Create edge
                    e = Edge(a, b)
                    
                    #Add edge to contour lines
                    contours.append(e)
                    
                #Edges p2p3 and p3p1 intersecting with plane        
                elif dz2 * dz3 <= 0 and dz3 * dz1 <= 0:         
                    #Compute intersetions
                    a = self.getContourPoint(p2, p3, z)
                    b = self.getContourPoint(p3, p1, z)
                    
                    #Create edge
                    e = Edge(a, b)
                    
                    #Add edge to contour lines
                    contours.append(e)
                    
                #Edges p3p1 and p1p2 intersecting with plane        
                elif dz3 * dz1 <= 0 and dz1 * dz2 <= 0:         
                    #Compute intersetions
                    a = self.getContourPoint(p3, p1, z)
                    b = self.getContourPoint(p1, p2, z)
                    
                    #Create edge
                    e = Edge(a, b)
                    
                    #Add edge to contour lines
                    contours.append(e)
                    
        return contours
                    
    def computeSlope(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF):       
        #Compute slope of a triangle
        #Directions
        ux = p1.x() - p2.x()
        uy = p1.y() - p2.y() 
        uz = p1.getZ() - p2.getZ() 
        
        vx = p3.x() - p2.x()
        vy = p3.y() - p2.y() 
        vz = p3.getZ() - p2.getZ() 
        
        #Normal vectors
        nx = uy * vz - vy * uz
        ny = - (ux * vz - vx * uz)
        nz = ux * vy - vx * uy
        
        #Normal vector norm
        norm = (nx**2 + ny**2 + nz**2)**(1/2)
        
        return acos(abs(nz)/norm)
    
    def computeAspect(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF):
        #Compute aspect of triangle
        #Directions
        ux = p1.x() - p2.x()
        uy = p1.y() - p2.y() 
        uz = p1.getZ() - p2.getZ() 
        
        vx = p3.x() - p2.x()
        vy = p3.y() - p2.y() 
        vz = p3.getZ() - p2.getZ() 
        
        #Normal vectors
        nx = uy * vz - vy * uz
        ny = - (ux * vz - vx * uz)    
        
        return atan2(nx, ny)
    
    def AnalyzeDTMSlope(self, dt:list[Edge]):
        #Analyze DTM slope
        
        dtm_slope:list[Triangle] = []
        #Process by triangles
        for i in range(0, len(dt), 3):
            #Vertices of triangle
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()
            
            #Get slope
            slope = self.computeSlope(p1, p2, p3)
            
            #Create triangle
            triangle = Triangle(p1, p2, p3, slope, 0)
            
            #Add triangle to list
            dtm_slope.append(triangle)
            
        return dtm_slope
    
    def AnalyzeDTMAspect(self, dt:list[Edge]):
            #Analyze DTM slope
            
        dtm_aspect:list[Triangle] = []
        #Process by triangles
        for i in range(0, len(dt), 3):
            #Vertices of triangle
            p1 = dt[i].getStart()
            p2 = dt[i].getEnd()
            p3 = dt[i+1].getEnd()
            
            #Get slope
            aspect = self.computeAspect(p1, p2, p3)
            
            #Create triangle
            triangle = Triangle(p1, p2, p3, 0, aspect)
            
            #Add triangle to list
            dtm_aspect.append(triangle)
                
        return dtm_aspect
            