from PyQt6 import QtCore, QtGui, QtWidgets
from draw import *
from algorithms import *
import geopandas as gpd
import matplotlib.pyplot as plt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(731, 554)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 731, 22))
        self.menubar.setObjectName("menubar")
        self.menuzadejte_soubor = QtWidgets.QMenu(parent=self.menubar)
        self.menuzadejte_soubor.setObjectName("menuzadejte_soubor")
        self.menuInput = QtWidgets.QMenu(parent=self.menubar)
        self.menuInput.setObjectName("menuInput")
        self.menuAnalyze = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionopen = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionopen.setIcon(icon)
        self.actionopen.setObjectName("actionopen")
        self.actionexit = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionexit.setIcon(icon1)
        self.actionexit.setObjectName("actionexit")
        self.actionClear = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/icons/clear_all.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon3)
        self.actionClear.setObjectName("actionClear")
        self.actionRay_Crossing = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/icons/ray.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRay_Crossing.setIcon(icon4)
        self.actionRay_Crossing.setObjectName("actionRay_Crossing")
        self.actionWinding_Number = QtGui.QAction(parent=MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/icons/winding.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWinding_Number.setIcon(icon5)
        self.actionWinding_Number.setObjectName("actionWinding_Number")
        self.menuzadejte_soubor.addAction(self.actionopen)
        self.menuzadejte_soubor.addAction(self.actionexit)
        self.menuInput.addSeparator()
        self.menuInput.addAction(self.actionClear)
        self.menuAnalyze.addAction(self.actionRay_Crossing)
        self.menuAnalyze.addAction(self.actionWinding_Number)
        self.menubar.addAction(self.menuzadejte_soubor.menuAction())
        self.menubar.addAction(self.menuInput.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.toolBar.addAction(self.actionopen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRay_Crossing)
        self.toolBar.addAction(self.actionWinding_Number)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionexit)

        self.retranslateUi(MainWindow)
        self.actionopen.triggered.connect(self.openClick) # type: ignore
        self.actionexit.triggered.connect(MainWindow.close) # type: ignore
        self.actionClear.triggered.connect(self.clearClick) # type: ignore
        self.actionWinding_Number.triggered.connect(self.windingNumberClick) # type: ignore
        self.actionRay_Crossing.triggered.connect(self.rayCrossingClick) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def openClick(self):
        self.Canvas.clearData()
        data = self.loadData()
        self.Canvas.loadData(data)
        
    def loadData(self):
        file, _ = QFileDialog.getOpenFileName(caption="Open File", directory="input/files/.", filter="Shapefile (*.shp)")
        data = gpd.read_file(file)
        return data
        
    def pointPolygonClick(self):
        # draw point or add vertex
        self.Canvas.switchDrawing()
        self.Canvas.repaint()
        
    def clearClick(self):
        # clear data
        self.Canvas.clearData()
    
    def rayCrossingClick(self):
        # get data
        q = self.Canvas.getQ()
        pol = self.Canvas.getPol()
        
        # analysis
        for i, polyg in enumerate(pol):
            res = Algorithms.analyzePointPolygonPosition(self, q, polyg)
            self.Canvas.polyg_status[i] = res
        
        # show result
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle("Analyze point and polygon position")
        
        # point inside
        for i in self.Canvas.polyg_status:
            if i:
                mb.setText("Point inside polygon")
                break
            
        # point outside
            else:
                mb.setText("Point outside polygon")
            
        # show window    
        mb.exec()
    
    def windingNumberClick(self):
        pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Point and polygon position"))
        self.menuzadejte_soubor.setTitle(_translate("MainWindow", "File"))
        self.menuInput.setTitle(_translate("MainWindow", "Input"))
        self.menuAnalyze.setTitle(_translate("MainWindow", "Analyze"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionopen.setText(_translate("MainWindow", "Open"))
        self.actionopen.setToolTip(_translate("MainWindow", "Open file"))
        self.actionexit.setText(_translate("MainWindow", "Exit"))
        self.actionexit.setToolTip(_translate("MainWindow", "Close app"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionRay_Crossing.setText(_translate("MainWindow", "Ray Crossing Algorithm"))
        self.actionWinding_Number.setText(_translate("MainWindow", "Winding Number Algorithm"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
