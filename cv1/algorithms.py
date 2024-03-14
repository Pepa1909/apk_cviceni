from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

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
        