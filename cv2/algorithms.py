from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np
import scipy.linalg as spl

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
        vy = p4.y() - p3.y()
        
        # dot product
        dot = ux * vx + uy * vy
        
        # norms of vectors
        nu = (ux * ux + uy * uy)**(1/2)
        nv = (vx * vx + vy * vy)**(1/2)
        
        # argument
        arg = dot/(nu*nv)
        
        if arg < -1:
            arg = -1
        elif arg > 1:
            arg = 1
        
        # OR
        
        return acos(arg)
    
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
                if qj != pol[i]:
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
    
    def getArea(self, pol:QPolygonF):
        # compute area of polygon
        area = 0
        n = len(pol)
        
        # process all points
        for i in range(n):
            area += pol[i].x() * (pol[(i+1)%n].y()-pol[(i-1+n)%n].y())   
            
        return abs(area)/2
    
    def resizeRectangle(self, rect:QPolygonF, build:QPolygonF):
        # resize rectangle to match area of building        
        # compute areas
        ab = self.getArea(build)
        a = self.getArea(rect)
        
        # compute area ratio
        k = ab/a
        
        # compute center of mass
        tx = (rect[0].x() + rect[1].x() + rect[2].x() + rect[3].x()) / 4
        ty = (rect[0].y() + rect[1].y() + rect[2].y() + rect[3].y()) / 4
        
        # vectors
        u1x = rect[0].x() - tx
        u1y = rect[0].y() - ty
        u2x = rect[1].x() - tx
        u2y = rect[1].y() - ty
        u3x = rect[2].x() - tx
        u3y = rect[2].y() - ty
        u4x = rect[3].x() - tx
        u4y = rect[3].y() - ty
        
        # new vertices
        v1x = tx + sqrt(k) * u1x
        v1y = ty + sqrt(k) * u1y
        v2x = tx + sqrt(k) * u2x
        v2y = ty + sqrt(k) * u2y
        v3x = tx + sqrt(k) * u3x
        v3y = ty + sqrt(k) * u3y
        v4x = tx + sqrt(k) * u4x
        v4y = ty + sqrt(k) * u4y
        
        v1 = QPointF(v1x, v1y)
        v2 = QPointF(v2x, v2y)
        v3 = QPointF(v3x, v3y)
        v4 = QPointF(v4x, v4y)
        
        # add vertices to polygon
        rect_r = QPolygonF([v1, v2, v3, v4])

        return rect_r
        
    def createMBR(self, pol:QPolygonF):
        # create minimum bounding rectangle
        # copmute convex hull
        ch = self.cHull(pol)
        n = len(ch)
                
        # inicialize min-max box
        mmb_min = self.minMaxBox(ch)
        area_min = self.getArea(mmb_min)
        sigma_min = 0
        
        # process all segmments of convex hull
        for i in range(n):
            dx = ch[(i+1)%n].x() - ch[i].x()
            dy = ch[(i+1)%n].y() - ch[i].y()
            
            # direction
            sigma = atan2(dy, dx)
            
            # rotate convex hull by -sigma
            ch_rot = self.rotate(ch, -sigma)
            
            # compute area of min-max box of rotated convex hull
            mmb_rot = self.minMaxBox(ch_rot)
            area_rot = self.getArea(mmb_rot)
            
            # smaller area?
            if area_rot < area_min:
                area_min = area_rot
                mmb_min = mmb_rot
                sigma_min = sigma
                
        # back rotation
        mmb_unrot = self.rotate(mmb_min, sigma_min)
        
        # resize rectangle
        mmb_res = self.resizeRectangle(mmb_unrot, pol)
        
        return mmb_res
    
    def createERPCA(self, pol:QPolygonF):
        # create enclosing rectangle using PCA
        # lists of coordinates
        x = []
        y = []
        
        # add coordinates to lists
        for p in pol:
            x.append(p.x())
            y.append(p.y())
            
        # create array
        P = np.array([x, y])
        
        # covariation matrix
        C = np.cov(P)
        
        # SVD
        U, S, V = spl.svd(C)
        
        # compute sigma
        sigma = atan2(V[0][1], V[0][0])
        
        # rotate polygon by -sigma
        pol_unrot = self.rotate(pol, -sigma)
        
        # create min-max box
        mmb = self.minMaxBox(pol_unrot)
        
        # rotate min-max box back
        er = self.rotate(mmb, sigma)
        
        # resize enclosing rectangle
        er_r = self.resizeRectangle(er, pol)
        
        return er_r
        