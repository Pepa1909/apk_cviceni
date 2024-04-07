from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np
import scipy.linalg as spl

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
    
    def jarvisScan(self, pol:QPolygonF):
        #Convex hull creation using Jarvis Scan
        ch = QPolygonF()
        
        #Find pivot 1
        q = min(pol, key = lambda k: k.y())
        
        #Find pivot 2 the safe way (width of data)
        p_max = max(pol, key = lambda k: k.x()) 
        p_min = min(pol, key = lambda k: k.x())
        
        data_w = p_max.x()-p_min.x()
        
        #Inicialize last two points of hull
        qj = q
        qj1 = QPointF(q.x() - data_w, q.y())
        
        #Add pivot to hull
        ch.append(q)
        
        #Find all points of hull
        while True:
            #Max and its index
            omega_max = 0
            index_max = -1            
            
            #Process all points and compute angle
            for i in range(len(pol)):
                if qj != pol[i]:
                    omega = self.get2LineAngle(qj, qj1, qj, pol[i])
                
                #Update maximum 
                    if omega > omega_max:
                        omega_max = omega
                        index_max = i
                    
            #Add point with maximum angle to hull
            ch.append(pol[index_max])
            
            #Found pivot again - convex hull is complete
            if pol[index_max] == q:
                break
            
            #Update last segment
            qj1 = qj
            qj = pol[index_max]
        
        return ch
    
    def minMaxBox(self, pol:QPolygonF):
        #Compute min_max box 
        #Find points with min and max coords
        px_min = min(pol, key = lambda k: k.x())
        px_max = max(pol, key = lambda k: k.x())
        
        py_min = min(pol, key = lambda k: k.y())
        py_max = max(pol, key = lambda k: k.y())
        
        #New points with extreme coordinates
        v1 = QPointF(px_min.x(), py_min.y())
        v2 = QPointF(px_max.x(), py_min.y())
        v3 = QPointF(px_max.x(), py_max.y())
        v4 = QPointF(px_min.x(), py_max.y())
        
        #Create min_max box
        box = QPolygonF([v1,v2,v3,v4])
        
        return box
    
    def rotate(self, pol:QPolygonF, sig:float):
        #Rotate polygon by given angle
        
        pol_r = QPolygonF()
        
        for p in pol:
            #Rotate point
            x_r = p.x() * cos(sig) - p.y() * sin(sig) 
            y_r = p.x() * sin(sig) + p.y() * cos(sig)

            #Create rotated point
            p_r = QPointF(x_r, y_r)
            
            #Add to rotated polygon
            pol_r.append(p_r)
            
        return pol_r
    
    def getArea(self, pol:QPolygonF):
        #Compute area of polygon
        area = 0
        n = len(pol)
        
        #Process all points
        for i in range(n):
            area += pol[i].x() * (pol[(i+1)%n].y()-pol[(i-1+n)%n].y())   
            
        return abs(area)/2
    
    def resizeRectangle(self, rect:QPolygonF, build:QPolygonF):
        #Resize rectangle to match area of building        
        #Compute areas
        ab = self.getArea(build)
        a = self.getArea(rect)
        
        #Compute area ratio
        k = ab/a
        
        #Compute center of mass
        tx = (rect[0].x() + rect[1].x() + rect[2].x() + rect[3].x()) / 4
        ty = (rect[0].y() + rect[1].y() + rect[2].y() + rect[3].y()) / 4
        
        #Vectors
        u1x = rect[0].x() - tx
        u1y = rect[0].y() - ty
        u2x = rect[1].x() - tx
        u2y = rect[1].y() - ty
        u3x = rect[2].x() - tx
        u3y = rect[2].y() - ty
        u4x = rect[3].x() - tx
        u4y = rect[3].y() - ty
        
        #New vertices
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
        
        #Add vertices to polygon
        rect_r = QPolygonF([v1, v2, v3, v4])

        return rect_r
        
    def createMBR(self, pol:QPolygonF):
        #Create minimum bounding rectangle
        #Copmute convex hull
        ch = self.jarvisScan(pol)
        n = len(ch)
                
        #Inicialize min-max box
        mmb_min = self.minMaxBox(ch)
        area_min = self.getArea(mmb_min)
        sigma_min = 0
        
        #Process all segmments of convex hull
        for i in range(n):
            dx = ch[(i+1)%n].x() - ch[i].x()
            dy = ch[(i+1)%n].y() - ch[i].y()
            
            #Direction
            sigma = atan2(dy, dx)
            
            #Rotate convex hull by -sigma
            ch_rot = self.rotate(ch, -sigma)
            
            #Compute area of min-max box of rotated convex hull
            mmb_rot = self.minMaxBox(ch_rot)
            area_rot = self.getArea(mmb_rot)
            
            #If the area is smaller than minimum, set new minimum and remember angle
            if area_rot < area_min:
                area_min = area_rot
                mmb_min = mmb_rot
                sigma_min = sigma
                
        #Back rotation
        mmb_unrot = self.rotate(mmb_min, sigma_min)
        
        #Resize rectangle
        mmb_res = self.resizeRectangle(mmb_unrot, pol)
        
        return mmb_res
    
    def createERPCA(self, pol:QPolygonF):
        #Create enclosing rectangle using PCA
        #Lists of coordinates
        x = []
        y = []
        
        #Add coordinates to lists
        for p in pol:
            x.append(p.x())
            y.append(p.y())
            
        #Create array
        P = np.array([x, y])
        
        #Compute covariation matrix
        C = np.cov(P)
        
        #SVD
        U, S, V = spl.svd(C)
        
        #Compute sigma
        sigma = atan2(V[0][1], V[0][0])
        
        #Rotate polygon by -sigma
        pol_unrot = self.rotate(pol, -sigma)
        
        #Create min-max box
        mmb = self.minMaxBox(pol_unrot)
        
        #Rotate min-max box back
        er = self.rotate(mmb, sigma)
        
        #Resize enclosing rectangle
        er_r = self.resizeRectangle(er, pol)
        
        return er_r
    
    def distance(self, p1:QPointF, p2:QPointF):
        #Compute Euclid distance of two points
        dist = sqrt((p2.x()-p1.x())**2 + (p2.y()-p1.y())**2)
        
        return dist
    
    def longestEdge(self, pol:QPolygonF):
        #Create enclosing rectangle using Longest Edge algorithm
        #Inicialize longest edge
        longest_edge = -1
        
        n = len(pol)
        
        #Process all edges
        for e in range(n):
            #Compute edge length
            e_len = self.distance(pol[e], pol[(e+1)%n])
            #If new edge is longer than maximum, set new maximum and remember its coordinates
            if e_len > longest_edge:
                longest_edge = e_len
                dx = pol[(e+1)%n].x() - pol[e].x()
                dy = pol[(e+1)%n].y() - pol[e].y()
        
        #Compute the angle of the longest edge
        sigma = atan2(dy, dx)
        
        #Rotate polygon by -sigma
        pol_rot = self.rotate(pol, -sigma)
        
        #Create min-max box
        mmb = self.minMaxBox(pol_rot)
        
        #Back rotation
        er = self.rotate(mmb, sigma)
        
        #Resize enclosing rectangle
        er_r = self.resizeRectangle(er, pol)
        
        return er_r
        
    def wallAverage(self, pol:QPolygonF):
        #Create enclosing rectangle using the Wall Average algorithm
        
        n = len(pol)
        #Compute angle of first edge
        dx = pol[1].x() - pol[0].x()
        dy = pol[1].y() - pol[0].y()
        sigma = atan2(dy, dx)
        
        #Set average remainder to 0
        r_sum = 0
        
        #Process all edges except the first one
        for e in range(1, n):
            dx_i = pol[(e+1)%n].x() - pol[e].x()
            dy_i = pol[(e+1)%n].y() - pol[e].y()
            
            #Compute angle of edge
            sigma_i = atan2(dy_i, dx_i)
            
            #Difference from initial slope
            d_sigma_i = sigma_i-sigma
            
            #Division by 2/pi and rounding to whole number
            k_i_r = round(d_sigma_i * pi/2)
            
            #Compute the remainder for segment
            r_i = (d_sigma_i * pi/2 - k_i_r) * pi/2
            
            #Add current remainder to sum of remainders
            r_sum += r_i
            
        #Compute artithmetic average of remainder    
        r_avg = r_sum / n
        
        #Compute average angle
        sigma_avg = sigma + r_avg
        
        #Rotate polygon by -sigma
        pol_rot = self.rotate(pol, -sigma_avg)
        
        #Create min-max box 
        mmb = self.minMaxBox(pol_rot)
        
        #Back rotation
        er = self.rotate(mmb, sigma_avg)
        
        #Resize enclosing rectangle
        er_r = self.resizeRectangle(er, pol)
        
        return er_r
    
    def weightedBisector(self, pol:QPolygonF):
        ch = self.jarvisScan(pol)
        
        diagonals = []
        
        n = len(ch)
        
        for i in range(n):
            for j in range(2, n-1):
                diagonals.append([ch[i], ch[j], self.distance(ch[i], ch[j])])
        
        diagonals.sort(key = lambda k: k[2], reverse=True)
        
        for diag in range(n):
            pass
            
        
        dx1 = diagonals[0][1].x() - diagonals[0][0].x()
        dy1 = diagonals[0][1].y() - diagonals[0][0].y()
        sigma1 = atan2(dy1, dx1)
        
        dx2 = diagonals[1][1].x() - diagonals[1][0].x()
        dy2 = diagonals[1][1].y() - diagonals[1][0].y()
        sigma2 = atan2(dy2, dx2)
        
        sigma = (sigma1 * diagonals[0][2] + sigma2 * diagonals[1][2]) / (diagonals[0][2] + diagonals[1][2])
        
        #Rotate polygon by -sigma
        pol_rot = self.rotate(pol, -sigma)
        
        #Create min-max box
        mmb = self.minMaxBox(pol_rot)
        
        #Back rotation
        er = self.rotate(mmb, sigma)
        
        #Resize enclosing rectangle
        er_r = self.resizeRectangle(er, pol)
        
        return er_r
        
    def orientation(self, p1:QPointF, p2:QPointF, p3:QPointF):
        pass