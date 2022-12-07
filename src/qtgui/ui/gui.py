# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.sidebarLeft = QtWidgets.QVBoxLayout()
        self.sidebarLeft.setObjectName("sidebarLeft")
        self.simulationsBox = QtWidgets.QComboBox(self.centralwidget)
        self.simulationsBox.setObjectName("simulationsBox")
        self.sidebarLeft.addWidget(self.simulationsBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.sidebarLeft.addItem(spacerItem)
        self.gridLayout.addLayout(self.sidebarLeft, 0, 0, 2, 1)
        self.graphicsLayout = GraphicsLayoutWidget(self.centralwidget)
        self.graphicsLayout.setStyleSheet("")
        self.graphicsLayout.setObjectName("graphicsLayout")
        self.gridLayout.addWidget(self.graphicsLayout, 0, 1, 1, 1)
        self.controlbarDown = QtWidgets.QWidget(self.centralwidget)
        self.controlbarDown.setObjectName("controlbarDown")
        self.controlbar = QtWidgets.QHBoxLayout(self.controlbarDown)
        self.controlbar.setObjectName("controlbar")
        self.startButton = QtWidgets.QPushButton(self.controlbarDown)
        self.startButton.setObjectName("startButton")
        self.controlbar.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.controlbarDown)
        self.stopButton.setObjectName("stopButton")
        self.controlbar.addWidget(self.stopButton)
        self.saveButton = QtWidgets.QPushButton(self.controlbarDown)
        self.saveButton.setObjectName("saveButton")
        self.controlbar.addWidget(self.saveButton)
        self.gridLayout.addWidget(self.controlbarDown, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 25))
        self.menubar.setObjectName("menubar")
        self.simulationMenu = QtWidgets.QMenu(self.menubar)
        self.simulationMenu.setObjectName("simulationMenu")
        self.visualisationMenu = QtWidgets.QMenu(self.menubar)
        self.visualisationMenu.setObjectName("visualisationMenu")
        MainWindow.setMenuBar(self.menubar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionDensity = QtGui.QAction(MainWindow)
        self.actionDensity.setObjectName("actionDensity")
        self.actionNavigation = QtGui.QAction(MainWindow)
        self.actionNavigation.setObjectName("actionNavigation")
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.simulationMenu.addAction(self.actionOpen)
        self.simulationMenu.addAction(self.actionSave)
        self.visualisationMenu.addAction(self.actionDensity)
        self.visualisationMenu.addAction(self.actionNavigation)
        self.menubar.addAction(self.simulationMenu.menuAction())
        self.menubar.addAction(self.visualisationMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        print("toto")

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Crowd Dynamics")
        self.startButton.setText("Start")
        self.stopButton.setText("Stop")
        self.saveButton.setText("Save")
        self.simulationMenu.setTitle("Simulation")
        self.visualisationMenu.setTitle("Visualisation")
        self.actionSave.setText("Save As")
        self.actionOpen.setText("Open")
        self.actionDensity.setText("Density")
        self.actionNavigation.setText("Navigation")
        self.actionNew.setText("New")

from pyqtgraph import GraphicsLayoutWidget
