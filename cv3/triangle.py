from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *

class Triangle:
    def __init__(self, p1:QPoint3DF, p2:QPoint3DF, p3:QPoint3DF, slope:float, exposition:float):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.slope = slope
        self.exposition = exposition
        
    def getP1(self):
        return self.p1
    
    def getP2(self):
        return self.p2
    
    def getP3(self):
        return self.p3