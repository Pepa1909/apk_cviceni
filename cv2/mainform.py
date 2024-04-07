
from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import *
import sys
import geopandas as gpd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(616, 454)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 616, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSimplify = QtWidgets.QMenu(parent=self.menubar)
        self.menuSimplify.setObjectName("menuSimplify")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionMinimum_Area_Enclosing_Rectangle = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/icons/maer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMinimum_Area_Enclosing_Rectangle.setIcon(icon2)
        self.actionMinimum_Area_Enclosing_Rectangle.setObjectName("actionMinimum_Area_Enclosing_Rectangle")
        self.actionPCA = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/icons/pca.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPCA.setIcon(icon3)
        self.actionPCA.setObjectName("actionPCA")
        self.actionClear_results = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/icons/clear_ch.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_results.setIcon(icon4)
        self.actionClear_results.setObjectName("actionClear_results")
        self.actionClear_all = QtGui.QAction(parent=MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/icons/clear_er.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_all.setIcon(icon5)
        self.actionClear_all.setObjectName("actionClear_all")
        self.actionLongest_Edge = QtGui.QAction(parent=MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/icons/longestedge.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionLongest_Edge.setIcon(icon6)
        self.actionLongest_Edge.setObjectName("actionLongest_Edge")
        self.actionWall_Average = QtGui.QAction(parent=MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWall_Average.setIcon(icon7)
        self.actionWall_Average.setObjectName("actionWall_Average")
        self.actionWeighted_Bisector = QtGui.QAction(parent=MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/icons/weightedbisector.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWeighted_Bisector.setIcon(icon8)
        self.actionWeighted_Bisector.setObjectName("actionWeighted_Bisector")
        self.actionJarvis_Scan = QtGui.QAction(parent=MainWindow)
        self.actionJarvis_Scan.setCheckable(False)
        self.actionJarvis_Scan.setObjectName("actionJarvis_Scan")
        self.actionGraham_Scan = QtGui.QAction(parent=MainWindow)
        self.actionGraham_Scan.setCheckable(False)
        self.actionGraham_Scan.setObjectName("actionGraham_Scan")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSimplify.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.menuSimplify.addAction(self.actionPCA)
        self.menuSimplify.addAction(self.actionLongest_Edge)
        self.menuSimplify.addAction(self.actionWall_Average)
        self.menuSimplify.addAction(self.actionWeighted_Bisector)
        self.menuView.addAction(self.actionClear_results)
        self.menuView.addAction(self.actionClear_all)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.toolBar.addAction(self.actionPCA)
        self.toolBar.addAction(self.actionLongest_Edge)
        self.toolBar.addAction(self.actionWall_Average)
        self.toolBar.addAction(self.actionWeighted_Bisector)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_results)
        self.toolBar.addAction(self.actionClear_all)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addSeparator()

        self.buttonJarvis = QtWidgets.QRadioButton(text="Jarvis Scan", checkable=True)
        self.buttonJarvis.setChecked(True)
        self.buttonJarvis.setToolTip("Construct convex hull using Jarvis Scan algorithm")
        self.buttonGraham = QtWidgets.QRadioButton(text="Graham Scan", checkable=True)
        self.buttonGraham.setToolTip("Construct convex hull using Graham Scan algorithm")
        # self.buttonJarvis.clicked.connect(self.switchToJarvis)
        # self.buttonGraham.clicked.connect(self.switchToGraham)
        self.group = QtWidgets.QButtonGroup(exclusive=True)
        for button in (self.buttonJarvis, self.buttonGraham):
            self.toolBar.addWidget(button)
            self.group.addButton(button)

        self.retranslateUi(MainWindow)
        self.actionOpen.triggered.connect(self.OpenClick) # type: ignore
        self.actionPCA.triggered.connect(self.pcaClick) # type: ignore
        self.actionMinimum_Area_Enclosing_Rectangle.triggered.connect(self.mbrClick) # type: ignore
        self.actionClear_all.triggered.connect(self.clearAllClick) # type: ignore
        self.actionClear_results.triggered.connect(self.clearClick) # type: ignore
        self.actionExit.triggered.connect(MainWindow.close) # type: ignore
        self.actionLongest_Edge.triggered.connect(self.longestEdgeClick) # type: ignore
        self.actionWall_Average.triggered.connect(self.wallAverageClick) # type: ignore
        self.actionWeighted_Bisector.triggered.connect(self.weightedBisectorClick) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
         
    def OpenClick(self):
        #Open file
        data = self.openFile()
        
        #If no file selected, return
        if data is None:
            return
        
        #Clear canvas for new polygon layer
        self.Canvas.clearAll()
        
        #Try to load and process the data
        correct_data = self.Canvas.loadData(data)
        
        #Alert the user if Shapefile is invalid
        if correct_data == False:
            dlg = QtWidgets.QMessageBox()
            dlg.setWindowTitle("Error Message")
            dlg.setText("Invalid Shapefile")
            dlg.exec()
            return
        
    def openFile(self):
        #Opens Shapefile
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", directory="input_files/.", filter="Shapefile (*.shp)")
        
        #Return if no file has been opened
        if filename == "":
            return None
        
        #Return data from shapefile
        data = gpd.read_file(filename)
        return data
    
    def mbrClick(self):
        #Displays MAERs using MBR algorithm
        self.Canvas.clearResults()
        
        #Get building list
        building_list = self.Canvas.getBuilding()
        
        #Warn user when no data are loaded
        if len(building_list) == 0:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle('Empty file')
            mb.setText("There are no buildings")
            mb.exec()
            return
        
        #Simplify all buildings
        a = Algorithms()
        for building in building_list:
            maer = a.createMBR(building)
            self.Canvas.mbr_list.append(maer)
        
        #Repaint screen
        self.Canvas.repaint()
    
    def pcaClick(self): # ctvrecove budovy spatne vysledky
        #Displays MAERs using PCA algorithm
        self.Canvas.clearResults()
        
        #Get building list
        building_list = self.Canvas.getBuilding()
        
        #Warn user when no data are loaded
        if len(building_list) == 0:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle('Empty file')
            mb.setText("There are no buildings")
            mb.exec()
            return
        
        #Simplify all buildings
        a = Algorithms()
        for building in building_list:
            maer = a.createERPCA(building)
            self.Canvas.mbr_list.append(maer)
        
        #Repaint screen
        self.Canvas.repaint()
        
    def longestEdgeClick(self):
        #Displays MAERs using the Longest Edge algorithm
        self.Canvas.clearResults()
        
        #Get building list
        building_list = self.Canvas.getBuilding()
        
        #Warn user when no data are loaded
        if len(building_list) == 0:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle('Empty file')
            mb.setText("There are no buildings")
            mb.exec()
            return
        
        #Simplify all buildings
        a = Algorithms()
        for building in building_list:
            maer = a.createLongestEdge(building)
            self.Canvas.mbr_list.append(maer)
        
        #Repaint screen
        self.Canvas.repaint()
    
    def wallAverageClick(self):
        #Displays MAERs using Wall Average algorithm
        self.Canvas.clearResults()
        
        #Get building list
        building_list = self.Canvas.getBuilding()
        
        #Warn user when no data are loaded
        if len(building_list) == 0:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle('Empty file')
            mb.setText("There are no buildings")
            mb.exec()
            return
        
        #Simplify all buildings
        a = Algorithms()
        for building in building_list:
            maer = a.createWallAverage(building)
            self.Canvas.mbr_list.append(maer)
            
        #Repaint screen
        self.Canvas.repaint()
            
    def weightedBisectorClick(self):
        #Displays MAERs using Weighted Bisector algorithm
        self.Canvas.clearResults()
        
        #Get building list
        building_list = self.Canvas.getBuilding()
        
        #Warn user when no data are loaded
        if len(building_list) == 0:
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle('Empty file')
            mb.setText("There are no buildings")
            mb.exec()
            return
        
        #Simplify all buildings
        a = Algorithms()
        for building in building_list:
            maer = a.weightedBisector(building)
            self.Canvas.mbr_list.append(maer)
        
        #Repaint screen
        self.Canvas.repaint()
    
    def clearClick(self):
        #Clear results
        self.Canvas.clearResults()
    
    def clearAllClick(self):
        #Clear results and data
        self.Canvas.clearAll()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSimplify.setTitle(_translate("MainWindow", "Simplify"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open file"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Close app"))
        self.actionMinimum_Area_Enclosing_Rectangle.setText(_translate("MainWindow", "Minimum Rectangle"))
        self.actionMinimum_Area_Enclosing_Rectangle.setToolTip(_translate("MainWindow", "Simplify using Minimum Rectangle"))
        self.actionPCA.setText(_translate("MainWindow", "PCA"))
        self.actionPCA.setToolTip(_translate("MainWindow", "Simplify using PCA"))
        self.actionClear_results.setText(_translate("MainWindow", "Clear results"))
        self.actionClear_all.setText(_translate("MainWindow", "Clear all"))
        self.actionLongest_Edge.setText(_translate("MainWindow", "Longest Edge"))
        self.actionWall_Average.setText(_translate("MainWindow", "Wall Average"))
        self.actionWeighted_Bisector.setText(_translate("MainWindow", "Weighted Bisector"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
