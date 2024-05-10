from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *

class Triangle:
    def __init__(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF, slope:float, aspect:float):
        self.vertices = []
        self.vertices.append(p1)
        self.vertices.append(p2)
        self.vertices.append(p3)
        self.slope = slope
        self.aspect = aspect
        
    def getVertices(self):
        return self.vertices
    
    def getSlope(self):
        return self.slope
    
    def getAspect(self):
        return self.aspect