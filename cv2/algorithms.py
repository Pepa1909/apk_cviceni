from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *

# processing data
class Algorithms:
    def __init__(self):
        pass
    
    def analyzePointPolygonPosition(self, q:QPointF, pol:QPolygonF):
        # inicialize intersection amount
        k = 0
         
        # amount of vertices
        n = len(pol)
         
        # process all segments
        for i in range(n):
             
            # reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
             
            xi1r = pol[(i+1)%n].x() - q.x() 
            yi1r = pol[(i+1)%n].y() - q.y() 
             
            # suitable segment?
            if ((yi1r > 0) and (yir <= 0)) or ((yir > 0) and (yi1r <= 0)):
                
                # compute intersection
                xm = (xi1r * yir - xir * yi1r)/(yi1r - yir)
                
                # right halfplane?
                if xm > 0:
                    k += 1
                    
        # q inside polygon
        if k%2 == 1:
            return True
        
        # q outside polygon
        return False
        
    def get2LineAngle(self, p1:QPointF,p2:QPointF,p3:QPointF,p4:QPointF):
        # compute angle of two lines
        # get parts of vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.x() - p3.y()
        
        # dot product
        dot = ux * vx + uy * vy
        
        # norms of vectors
        nu = (ux * ux + uy * uy)**(1/2)
        nv = (vx * vx + vy * vy)**(1/2)
        
        # angle phi
        return acos(dot/(nu*nv))
    
    def cHull(self, pol:QPolygonF):
        # convex hull creation using Jarvis Scan
        ch = QPolygonF()
        
        # find pivot 1
        q = min(pol, key = lambda k: k.y())
        
        # find pivot 2
        s = min(pol, key = lambda k: k.x())
        
        # inicialize last two points of hull
        qj = q
        qj1 = QPointF(s.x(), q.y())
        
        # add pivot to hull
        ch.append(q)
        
        # find all points of hull
        while True:
            # max and its index
            omega_max = 0
            index_max = -1            
            
            # process all points
            for i in range(len(pol)):
                omega = self.get2LineAngle(qj, qj1, qj, pol[i])
                
                # update maximum
                if omega > omega_max:
                    omega_max = omega
                    index_max = i
                    
            # add point to hull
            ch.append(pol[index_max])
            
            # found pivot again
            if pol[index_max] == q:
                break
            
            # update last segment
            qj1 = qj
            qj = pol[index_max]
        
        return ch
    
    def minMaxBox(self, pol:QPolygonF):
        # compute min_max box 
        # find points with min and max coords
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
    
    def rotate(self, pol:QPolygonF, sig:float):
        # rotate polygon by given angle
        
        pol_r = QPolygonF()
        
        for p in pol:
            # rotate point
            x_r = p.x() * cos(sig) - p.y() * sin(sig) 
            y_r = p.x() * sin(sig) + p.y() * cos(sig)

            # create rotated point
            p_r = QPointF(x_r, y_r)
            
            # add to polygon
            pol_r.append(p_r)
            
        return pol_r