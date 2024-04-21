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
    
    
    def grahamScan(self, pol:QPolygonF):
        #Convex hull creation using Graham Scan 
        #Find pivot
        q = min(pol, key=lambda k: k.y())
        
        #Create list of points
        points = []
        for p in pol:
            points.append(p)
        
        #Sort points by their angle and secondary by distance from pivot
        points.sort(key=lambda k: (self.computeSlope(q, k), self.distance(q, k)))
        
        #Create list for convex hull points
        ch_list = []
        n = len(pol)
        
        #Iterate over all points
        for i in range(n):
            #Makes sure to append first two points
            while len(ch_list) >= 2:
                #Checks if point is in left half-plane
                if self.getPointAndLinePosition(ch_list[-2], ch_list[-1], points[i]):
                    break
                #Removes last appended point if not in left half-plane
                ch_list.pop()
            #Appends next point
            ch_list.append(points[i])
        
        #Append pivot to match Jarvis Scan creation
        ch_list.append(q)
        
        #Create polygon from list
        ch = QPolygonF(ch_list)
        
        return ch
    

    def createMBR(self, pol:QPolygonF):
        #Create minimum bounding rectangle
        #Copmute convex hull
        ch = self.ch_method(pol)
        n = len(ch)
                
        #Inicialize min-max box
        mmb_min = self.minMaxBox(ch)
        area_min = self.getArea(mmb_min)
        sigma_min = 0
        
        #Process all segmments of convex hull
        for i in range(n):
            
            #Direction
            sigma = self.computeSlope(ch[(i+1)%n], ch[i])
            
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
    
    
    def createLongestEdge(self, pol:QPolygonF):
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
        
        
    def createWallAverage(self, pol:QPolygonF):
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
                
            #pi/2 multiplication
            k_i = d_sigma_i * 2/pi
            
            #Compute the remainder for segment
            r_i = (k_i - round(k_i)) * pi/2
            
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
    
    
    def createWeightedBisector(self, pol:QPolygonF):
        #Create enclosing rectangle using the Weighted Bisector algorithm
        #Create convex hull of polygon
        ch = self.ch_method(pol)
        
        #Initialize diagonals list
        diagonals_of_ch = []
        
        #Iterate over all points (length-1 because the first and last points are identical)
        n = len(ch)-1
        for i in range(n):
            #Iterate over all points
            for j in range(n):
                #Check for neighboring points and self
                if i != j and i+1 != j and i-1 != j:
                    #Create diagonal and remember its length
                    diag = [ch[i], ch[j], self.distance(ch[i], ch[j])]
                    #Chceck if the diagonal is not already in list
                    if [diag[1], diag[0], diag[2]] not in diagonals_of_ch:
                        diagonals_of_ch.append(diag)
        
        #List for real diagonals - created list contains diagonals of Convex Hull
        real_diagonals = []
        
        #Iterate over all diagonals
        for i in range(len(diagonals_of_ch)):
            #Iterate over all points of polygon
            for j in range(len(pol)):
                #Don't consider diagonals with common points
                if (diagonals_of_ch[i][0] != pol[j]) and (diagonals_of_ch[i][1] != pol[(j+1)%len(pol)]): 
                    crossing = self.intersect(diagonals_of_ch[i][0], diagonals_of_ch[i][1], pol[j], pol[(j+1)%len(pol)])
                    #If diagonal and polygon edge do not intersect, add to new list
                    if crossing == False:
                        real_diagonals.append(diagonals_of_ch[i])
                        break
            
        #Sort diagonals by length
        real_diagonals.sort(key = lambda k: k[2], reverse=True)
        
        #Compute vectors and their slope
        dx1 = real_diagonals[0][1].x() - real_diagonals[0][0].x()
        dy1 = real_diagonals[0][1].y() - real_diagonals[0][0].y()
        sigma1 = atan2(dy1, dx1)
        
        #Check if second longest diagonal doesn't share a point with the longest
        for i in range(len(real_diagonals)):
            if (real_diagonals[i][0] != real_diagonals[0][0]) and (real_diagonals[i][1] != real_diagonals[0][1]):
                dx2 = real_diagonals[i][1].x() - real_diagonals[i][0].x()
                dy2 = real_diagonals[i][1].y() - real_diagonals[i][0].y()
                sigma2 = atan2(dy2, dx2)
                break
        
        #Final slope based weighted by lenghts of diagonals
        sigma = (sigma1 * real_diagonals[0][2] + sigma2 * real_diagonals[i][2]) / (real_diagonals[0][2] + real_diagonals[i][2])
        
        #Rotate polygon by -sigma
        pol_rot = self.rotate(pol, -sigma)
        
        #Create min-max box
        mmb = self.minMaxBox(pol_rot)
        
        #Back rotation
        er = self.rotate(mmb, sigma)
        
        #Resize enclosing rectangle
        er_r = self.resizeRectangle(er, pol)
        
        return er_r
     
    
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
        
   
    def distance(self, p1:QPointF, p2:QPointF):
        #Compute Euclid distance of two points
        dist = sqrt((p2.x()-p1.x())**2 + (p2.y()-p1.y())**2)
        
        return dist
    
   
    def intersect(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Determines if two given segments (p1p2 and p3p4) intersect
        #Compute determinants
        t1 = (p2.x() - p1.x()) * (p4.y() - p1.y()) - (p4.x() - p1.x()) * (p2.y() - p1.y())
        t2 = (p2.x() - p1.x()) * (p3.y() - p1.y()) - (p3.x() - p1.x()) * (p2.y() - p1.y())
        t3 = (p4.x() - p3.x()) * (p1.y() - p3.y()) - (p1.x() - p3.x()) * (p4.y() - p3.y())
        t4 = (p4.x() - p3.x()) * (p2.y() - p3.y()) - (p2.x() - p3.x()) * (p4.y() - p3.y())
        
        #The intersection exists, if determinants have different signs
        if t1 * t2 >= 0 or t3 * t4 >= 0:
            return False
        
        return True
    
    
    def computeSlope(self, p1:QPointF, p2:QPointF):
        #Computes slope of two points
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()

        return atan2(dy, dx)
    
    
    def getPointAndLinePosition(self, p:QPointF, p1:QPointF, p2:QPointF):
        #Determines if point p is in left half-plane from segment p1p2
        #Compute vectors
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
    
    
    def mainDirection(self, mbr: QPolygonF):
        #Calculate main direction based on longest edge of MAER
        max_len = 0
        max_angle = 0
        
        #Iterate over all points
        n = len(mbr)
        for i in range(n):
            #Calculate length of edge
            edge_len = self.distance(mbr[(i+1)%n], mbr[i])
            #If current edge longer, update longest edge and comupte its angle
            if edge_len > max_len:
                max_len = edge_len
                max_angle = self.computeSlope(mbr[(i+1)%n], mbr[i])
                
        return max_angle
            
    
    def evaluation(self, pol:QPolygonF, mbr: QPolygonF):
        #Evaluate the precision of algorithm based on means
        #Compute main direction of MAER
        sigma_rect = self.mainDirection(mbr)
        
        #Compute k and r of rectangle
        k = 2 * sigma_rect / pi
        r = (k - round(k)) * (pi/2)
        
        r_sum = 0
        
        #Iterate over all points
        n = len(pol)
        for i in range(n):
            dx_i = pol[(i+1)%n].x() - pol[i].x()
            dy_i = pol[(i+1)%n].y() - pol[i].y()
            
            #Compute angle of edge
            sigma_i = atan2(dy_i, dx_i)
            
            #Multiply by 2/pi
            k_i = 2 * sigma_i / pi
            
            #Compute the remainder
            r_i = (k_i - round(k_i)) * (pi/2)
            
            #Add remainder to sum of remainders
            r_sum += (r_i - r)
            
        #Mean angle
        d_sigma = pi / (2*n) * r_sum
        
        #Compute it in degrees
        d_sigma_deg = abs(d_sigma * 180/pi)
        
        #Find effective and non-effective bounding rectangles
        if d_sigma_deg < 10:
            return 1
        
        return 0
    
    def evaluation2(self, pol:QPolygonF, mbr: QPolygonF):
        #Evaluate the precision of algorithm based on squared means
        #Compute main direction of MAER
        sigma_rect = self.mainDirection(mbr)
        
        #Compute k and r of rectangle
        k = 2 * sigma_rect / pi
        r = (k - round(k)) * (pi/2)
        
        r_sum = 0
        
        #Iterate over all points
        n = len(pol)
        for i in range(n):
            dx_i = pol[(i+1)%n].x() - pol[i].x()
            dy_i = pol[(i+1)%n].y() - pol[i].y()
            
            #Compute angle of edge
            sigma_i = atan2(dy_i, dx_i)
            
            #Multiply by 2/pi
            k_i = 2 * sigma_i / pi
            
            #Compute the remainder
            r_i = (k_i - round(k_i)) * (pi/2)
            
            #Add remainder to sum of remainders
            r_sum += (r_i - r)**2
        
        #Mean Squared angle
        d_sigma = pi / (2*n) * sqrt(r_sum)
        
        #Compute it in degrees
        d_sigma_deg = abs(d_sigma * 180/pi)

        #Find effective and non-effective bounding rectangles
        if d_sigma_deg < 10:
            return 1
        
        return 0
        
    #Set default convex hull algorithm to Jarvis Scan
    ch_method = jarvisScan