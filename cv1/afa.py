import geopandas as gpd
import numpy as np
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

data = gpd.read_file("okresy\Okresy_-_polygony.shp")
polygony = data.geometry
all_pols = QPolygonF
for index, pol in enumerate(polygony):
    g = [i for i in polygony]
    if pol.geom_type == "Polygon":
        x,y = g[index].exterior.coords.xy
    else:
        x,y = g[index].convex_hull.exterior.coords.xy    
    coords = np.dstack((x,y)).tolist()
    for i in coords[0]:
        p = QPointF(i[0],-i[1])
        all_pols.append(p)
len(all_pols)