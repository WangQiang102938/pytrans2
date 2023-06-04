# Form implementation generated from reading ui file './mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.5.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1407, 1029)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.previewContainer = QtWidgets.QGroupBox(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewContainer.sizePolicy().hasHeightForWidth())
        self.previewContainer.setSizePolicy(sizePolicy)
        self.previewContainer.setMinimumSize(QtCore.QSize(400, 800))
        self.previewContainer.setCheckable(False)
        self.previewContainer.setObjectName("previewContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.previewContainer)
        self.gridLayout_2.setSpacing(20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.previewImageContainer = QtWidgets.QGroupBox(parent=self.previewContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewImageContainer.sizePolicy().hasHeightForWidth())
        self.previewImageContainer.setSizePolicy(sizePolicy)
        self.previewImageContainer.setObjectName("previewImageContainer")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.previewImageContainer)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.previewImage = QtWidgets.QGraphicsView(parent=self.previewImageContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.previewImage.sizePolicy().hasHeightForWidth())
        self.previewImage.setSizePolicy(sizePolicy)
        self.previewImage.setMouseTracking(True)
        self.previewImage.setObjectName("previewImage")
        self.gridLayout_7.addWidget(self.previewImage, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.previewImageContainer, 2, 0, 1, 1)
        self.previewControlContainer = QtWidgets.QGroupBox(parent=self.previewContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewControlContainer.sizePolicy().hasHeightForWidth())
        self.previewControlContainer.setSizePolicy(sizePolicy)
        self.previewControlContainer.setFlat(False)
        self.previewControlContainer.setObjectName("previewControlContainer")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.previewControlContainer)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalGroupBox_2 = QtWidgets.QGroupBox(parent=self.previewControlContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalGroupBox_2.sizePolicy().hasHeightForWidth())
        self.horizontalGroupBox_2.setSizePolicy(sizePolicy)
        self.horizontalGroupBox_2.setObjectName("horizontalGroupBox_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalGroupBox_2)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.previewPrevButton = QtWidgets.QToolButton(parent=self.horizontalGroupBox_2)
        self.previewPrevButton.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.previewPrevButton.setObjectName("previewPrevButton")
        self.horizontalLayout_4.addWidget(self.previewPrevButton)
        self.previewPageMeter = QtWidgets.QLabel(parent=self.horizontalGroupBox_2)
        self.previewPageMeter.setMinimumSize(QtCore.QSize(16, 0))
        self.previewPageMeter.setText("")
        self.previewPageMeter.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.previewPageMeter.setObjectName("previewPageMeter")
        self.horizontalLayout_4.addWidget(self.previewPageMeter)
        self.previewNextButton = QtWidgets.QToolButton(parent=self.horizontalGroupBox_2)
        self.previewNextButton.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.previewNextButton.setObjectName("previewNextButton")
        self.horizontalLayout_4.addWidget(self.previewNextButton)
        self.label_11 = QtWidgets.QLabel(parent=self.horizontalGroupBox_2)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.zoomInButton = QtWidgets.QToolButton(parent=self.horizontalGroupBox_2)
        self.zoomInButton.setObjectName("zoomInButton")
        self.horizontalLayout_4.addWidget(self.zoomInButton)
        self.zoomFitButton = QtWidgets.QToolButton(parent=self.horizontalGroupBox_2)
        self.zoomFitButton.setCheckable(True)
        self.zoomFitButton.setObjectName("zoomFitButton")
        self.horizontalLayout_4.addWidget(self.zoomFitButton)
        self.zoomOutButton = QtWidgets.QToolButton(parent=self.horizontalGroupBox_2)
        self.zoomOutButton.setObjectName("zoomOutButton")
        self.horizontalLayout_4.addWidget(self.zoomOutButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.docCloseButton = QtWidgets.QToolButton(parent=self.horizontalGroupBox_2)
        self.docCloseButton.setObjectName("docCloseButton")
        self.horizontalLayout_4.addWidget(self.docCloseButton)
        self.verticalLayout_7.addWidget(self.horizontalGroupBox_2)
        self.captureControlCon = QtWidgets.QGroupBox(parent=self.previewControlContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captureControlCon.sizePolicy().hasHeightForWidth())
        self.captureControlCon.setSizePolicy(sizePolicy)
        self.captureControlCon.setObjectName("captureControlCon")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.captureControlCon)
        self.horizontalLayout_7.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.captureCreateBtn = QtWidgets.QToolButton(parent=self.captureControlCon)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captureCreateBtn.sizePolicy().hasHeightForWidth())
        self.captureCreateBtn.setSizePolicy(sizePolicy)
        self.captureCreateBtn.setCheckable(True)
        self.captureCreateBtn.setObjectName("captureCreateBtn")
        self.horizontalLayout_7.addWidget(self.captureCreateBtn)
        self.captureSelectCombo = QtWidgets.QComboBox(parent=self.captureControlCon)
        self.captureSelectCombo.setObjectName("captureSelectCombo")
        self.horizontalLayout_7.addWidget(self.captureSelectCombo)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.captureDelBtn = QtWidgets.QToolButton(parent=self.captureControlCon)
        self.captureDelBtn.setAutoRaise(False)
        self.captureDelBtn.setObjectName("captureDelBtn")
        self.horizontalLayout_7.addWidget(self.captureDelBtn)
        self.captureDelBtn.raise_()
        self.captureCreateBtn.raise_()
        self.captureSelectCombo.raise_()
        self.verticalLayout_7.addWidget(self.captureControlCon)
        self.gridLayout_2.addWidget(self.previewControlContainer, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.previewContainer, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1407, 24))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusBar.setSizeGripEnabled(True)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.settingDockCon = QtWidgets.QDockWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingDockCon.sizePolicy().hasHeightForWidth())
        self.settingDockCon.setSizePolicy(sizePolicy)
        self.settingDockCon.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.settingDockCon.setObjectName("settingDockCon")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.dockWidgetContents_4)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.controlPanelContainer = QtWidgets.QTabWidget(parent=self.dockWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlPanelContainer.sizePolicy().hasHeightForWidth())
        self.controlPanelContainer.setSizePolicy(sizePolicy)
        self.controlPanelContainer.setMinimumSize(QtCore.QSize(400, 800))
        self.controlPanelContainer.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.controlPanelContainer.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.controlPanelContainer.setObjectName("controlPanelContainer")
        self.controlPanelContainerPage1 = QtWidgets.QWidget()
        self.controlPanelContainerPage1.setObjectName("controlPanelContainerPage1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.controlPanelContainerPage1)
        self.gridLayout_4.setSpacing(20)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.optionContainer = QtWidgets.QGroupBox(parent=self.controlPanelContainerPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.optionContainer.sizePolicy().hasHeightForWidth())
        self.optionContainer.setSizePolicy(sizePolicy)
        self.optionContainer.setObjectName("optionContainer")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.optionContainer)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.nodeTabC = QtWidgets.QTabWidget(parent=self.optionContainer)
        self.nodeTabC.setObjectName("nodeTabC")
        self.nodePreviewTab = QtWidgets.QWidget()
        self.nodePreviewTab.setObjectName("nodePreviewTab")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.nodePreviewTab)
        self.gridLayout_11.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_11.setSpacing(6)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.capturePreviewImage = QtWidgets.QGraphicsView(parent=self.nodePreviewTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.capturePreviewImage.sizePolicy().hasHeightForWidth())
        self.capturePreviewImage.setSizePolicy(sizePolicy)
        self.capturePreviewImage.setObjectName("capturePreviewImage")
        self.gridLayout_11.addWidget(self.capturePreviewImage, 0, 0, 1, 1)
        self.nodeTabC.addTab(self.nodePreviewTab, "")
        self.nodeOptionC = QtWidgets.QWidget()
        self.nodeOptionC.setObjectName("nodeOptionC")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.nodeOptionC)
        self.verticalLayout_5.setContentsMargins(12, -1, 12, 12)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.nodeTabC.addTab(self.nodeOptionC, "")
        self.gridLayout_6.addWidget(self.nodeTabC, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.optionContainer, 1, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.controlPanelContainerPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_12.setSpacing(6)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.capturedItemTree = QtWidgets.QTreeWidget(parent=self.groupBox_2)
        self.capturedItemTree.setColumnCount(1)
        self.capturedItemTree.setObjectName("capturedItemTree")
        self.capturedItemTree.headerItem().setText(0, "1")
        self.gridLayout_12.addWidget(self.capturedItemTree, 2, 0, 1, 1)
        self.widget_3 = QtWidgets.QWidget(parent=self.groupBox_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.comboBox = QtWidgets.QComboBox(parent=self.widget_3)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_9.addWidget(self.comboBox)
        self.toolButton_2 = QtWidgets.QToolButton(parent=self.widget_3)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_9.addWidget(self.toolButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.toolButton_3 = QtWidgets.QToolButton(parent=self.widget_3)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout_9.addWidget(self.toolButton_3)
        self.gridLayout_12.addWidget(self.widget_3, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 2)
        self.controlPanelContainer.addTab(self.controlPanelContainerPage1, "")
        self.ioTab = QtWidgets.QWidget()
        self.ioTab.setObjectName("ioTab")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.ioTab)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.ioModuleTab = QtWidgets.QTabWidget(parent=self.ioTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ioModuleTab.sizePolicy().hasHeightForWidth())
        self.ioModuleTab.setSizePolicy(sizePolicy)
        self.ioModuleTab.setObjectName("ioModuleTab")
        self.verticalLayout_10.addWidget(self.ioModuleTab)
        self.groupBox = QtWidgets.QGroupBox(parent=self.ioTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.openedDocList = QtWidgets.QListWidget(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openedDocList.sizePolicy().hasHeightForWidth())
        self.openedDocList.setSizePolicy(sizePolicy)
        self.openedDocList.setObjectName("openedDocList")
        self.horizontalLayout_6.addWidget(self.openedDocList)
        self.verticalLayout_10.addWidget(self.groupBox)
        self.groupBox_21 = QtWidgets.QGroupBox(parent=self.ioTab)
        self.groupBox_21.setObjectName("groupBox_21")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_21)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(parent=self.groupBox_21)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.groupBox_21)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.groupBox_21)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_10.addWidget(self.groupBox_21)
        self.controlPanelContainer.addTab(self.ioTab, "")
        self.gridLayout_19.addWidget(self.controlPanelContainer, 0, 0, 1, 1)
        self.settingDockCon.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.settingDockCon)
        self.outputDockCon = QtWidgets.QDockWidget(parent=MainWindow)
        self.outputDockCon.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.outputDockCon.setObjectName("outputDockCon")
        self.dockWidgetContents_6 = QtWidgets.QWidget()
        self.dockWidgetContents_6.setObjectName("dockWidgetContents_6")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.dockWidgetContents_6)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.widget_4 = QtWidgets.QWidget(parent=self.dockWidgetContents_6)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pipeRunNodeBtn = QtWidgets.QPushButton(parent=self.widget_4)
        self.pipeRunNodeBtn.setObjectName("pipeRunNodeBtn")
        self.horizontalLayout_3.addWidget(self.pipeRunNodeBtn)
        self.pipeRunBtn = QtWidgets.QPushButton(parent=self.widget_4)
        self.pipeRunBtn.setObjectName("pipeRunBtn")
        self.horizontalLayout_3.addWidget(self.pipeRunBtn)
        self.gridLayout_22.addWidget(self.widget_4, 2, 0, 1, 1)
        self.frame = QtWidgets.QFrame(parent=self.dockWidgetContents_6)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_5.setHorizontalSpacing(4)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pipeProgress = QtWidgets.QProgressBar(parent=self.frame)
        self.pipeProgress.setProperty("value", 0)
        self.pipeProgress.setObjectName("pipeProgress")
        self.gridLayout_5.addWidget(self.pipeProgress, 1, 1, 1, 1)
        self.pipeCapNodeProgress = QtWidgets.QProgressBar(parent=self.frame)
        self.pipeCapNodeProgress.setProperty("value", 0)
        self.pipeCapNodeProgress.setObjectName("pipeCapNodeProgress")
        self.gridLayout_5.addWidget(self.pipeCapNodeProgress, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.frame)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 1, 0, 1, 1)
        self.gridLayout_22.addWidget(self.frame, 1, 0, 1, 1)
        self.tabWidget_2 = QtWidgets.QTabWidget(parent=self.dockWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.pipeEditTab = QtWidgets.QWidget()
        self.pipeEditTab.setObjectName("pipeEditTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pipeEditTab)
        self.verticalLayout_4.setContentsMargins(-1, 4, -1, 4)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pipeAvaliableCombo = QtWidgets.QComboBox(parent=self.pipeEditTab)
        self.pipeAvaliableCombo.setObjectName("pipeAvaliableCombo")
        self.verticalLayout_4.addWidget(self.pipeAvaliableCombo)
        self.widget = QtWidgets.QWidget(parent=self.pipeEditTab)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(8, 4, 8, 4)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.PipeAddBtn = QtWidgets.QToolButton(parent=self.widget)
        self.PipeAddBtn.setObjectName("PipeAddBtn")
        self.horizontalLayout.addWidget(self.PipeAddBtn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.PipeUpBtn = QtWidgets.QToolButton(parent=self.widget)
        self.PipeUpBtn.setObjectName("PipeUpBtn")
        self.horizontalLayout.addWidget(self.PipeUpBtn)
        self.PipeDownBtn = QtWidgets.QToolButton(parent=self.widget)
        self.PipeDownBtn.setObjectName("PipeDownBtn")
        self.horizontalLayout.addWidget(self.PipeDownBtn)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.PipeRemoveBtn = QtWidgets.QToolButton(parent=self.widget)
        self.PipeRemoveBtn.setObjectName("PipeRemoveBtn")
        self.horizontalLayout.addWidget(self.PipeRemoveBtn)
        self.verticalLayout_4.addWidget(self.widget)
        self.pipeEditList = QtWidgets.QListWidget(parent=self.pipeEditTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.pipeEditList.sizePolicy().hasHeightForWidth())
        self.pipeEditList.setSizePolicy(sizePolicy)
        self.pipeEditList.setObjectName("pipeEditList")
        self.verticalLayout_4.addWidget(self.pipeEditList)
        self.tabWidget = QtWidgets.QTabWidget(parent=self.pipeEditTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_9.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pipeOptionContainer = QtWidgets.QGroupBox(parent=self.tab_2)
        self.pipeOptionContainer.setTitle("")
        self.pipeOptionContainer.setObjectName("pipeOptionContainer")
        self.verticalLayout_9.addWidget(self.pipeOptionContainer)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_8.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pipeLinkEditCon = QtWidgets.QGroupBox(parent=self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pipeLinkEditCon.sizePolicy().hasHeightForWidth())
        self.pipeLinkEditCon.setSizePolicy(sizePolicy)
        self.pipeLinkEditCon.setMinimumSize(QtCore.QSize(0, 40))
        self.pipeLinkEditCon.setTitle("")
        self.pipeLinkEditCon.setObjectName("pipeLinkEditCon")
        self.verticalLayout_8.addWidget(self.pipeLinkEditCon)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.widget_2 = QtWidgets.QWidget(parent=self.pipeEditTab)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pipeConfigLoadBtn = QtWidgets.QToolButton(parent=self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pipeConfigLoadBtn.sizePolicy().hasHeightForWidth())
        self.pipeConfigLoadBtn.setSizePolicy(sizePolicy)
        self.pipeConfigLoadBtn.setObjectName("pipeConfigLoadBtn")
        self.horizontalLayout_5.addWidget(self.pipeConfigLoadBtn)
        self.pipeConfigSaveBtn = QtWidgets.QToolButton(parent=self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pipeConfigSaveBtn.sizePolicy().hasHeightForWidth())
        self.pipeConfigSaveBtn.setSizePolicy(sizePolicy)
        self.pipeConfigSaveBtn.setObjectName("pipeConfigSaveBtn")
        self.horizontalLayout_5.addWidget(self.pipeConfigSaveBtn)
        self.verticalLayout_4.addWidget(self.widget_2)
        self.tabWidget_2.addTab(self.pipeEditTab, "")
        self.pipeNodeEditTab = QtWidgets.QWidget()
        self.pipeNodeEditTab.setObjectName("pipeNodeEditTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.pipeNodeEditTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pipeOptionViewList = QtWidgets.QListWidget(parent=self.pipeNodeEditTab)
        self.pipeOptionViewList.setObjectName("pipeOptionViewList")
        self.verticalLayout_6.addWidget(self.pipeOptionViewList)
        self.pipeOptionTabC = QtWidgets.QTabWidget(parent=self.pipeNodeEditTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.pipeOptionTabC.sizePolicy().hasHeightForWidth())
        self.pipeOptionTabC.setSizePolicy(sizePolicy)
        self.pipeOptionTabC.setObjectName("pipeOptionTabC")
        self.pipeOptionTab = QtWidgets.QWidget()
        self.pipeOptionTab.setObjectName("pipeOptionTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pipeOptionTab)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pipeOptionTabC.addTab(self.pipeOptionTab, "")
        self.pipeNodeMemoC = QtWidgets.QWidget()
        self.pipeNodeMemoC.setObjectName("pipeNodeMemoC")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.pipeNodeMemoC)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pipeMemoSelectTabC = QtWidgets.QTabWidget(parent=self.pipeNodeMemoC)
        self.pipeMemoSelectTabC.setObjectName("pipeMemoSelectTabC")
        self.pipeDefaultMemoCon = QtWidgets.QWidget()
        self.pipeDefaultMemoCon.setObjectName("pipeDefaultMemoCon")
        self.pipeMemoSelectTabC.addTab(self.pipeDefaultMemoCon, "")
        self.pipeCapNodeMemoCon = QtWidgets.QWidget()
        self.pipeCapNodeMemoCon.setObjectName("pipeCapNodeMemoCon")
        self.pipeMemoSelectTabC.addTab(self.pipeCapNodeMemoCon, "")
        self.verticalLayout.addWidget(self.pipeMemoSelectTabC)
        self.pipeOptionTabC.addTab(self.pipeNodeMemoC, "")
        self.pipeOutputTab = QtWidgets.QWidget()
        self.pipeOutputTab.setObjectName("pipeOutputTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pipeOutputTab)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.plainTextEdit = QCodeEditor(parent=self.pipeOutputTab)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_3.addWidget(self.plainTextEdit)
        self.pipeOptionTabC.addTab(self.pipeOutputTab, "")
        self.verticalLayout_6.addWidget(self.pipeOptionTabC)
        self.tabWidget_2.addTab(self.pipeNodeEditTab, "")
        self.gridLayout_22.addWidget(self.tabWidget_2, 0, 0, 1, 1)
        self.outputDockCon.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.outputDockCon)
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(parent=MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.controlPanelContainer.setCurrentIndex(1)
        self.nodeTabC.setCurrentIndex(1)
        self.ioModuleTab.setCurrentIndex(-1)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.pipeOptionTabC.setCurrentIndex(0)
        self.pipeMemoSelectTabC.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.previewContainer.setTitle(_translate("MainWindow", "Preview"))
        self.previewImageContainer.setTitle(_translate("MainWindow", "Preview"))
        self.previewControlContainer.setTitle(_translate("MainWindow", "Control"))
        self.horizontalGroupBox_2.setTitle(_translate("MainWindow", "Doc Control"))
        self.previewPrevButton.setText(_translate("MainWindow", "<"))
        self.previewNextButton.setText(_translate("MainWindow", ">"))
        self.label_11.setText(_translate("MainWindow", "Zoom:"))
        self.zoomInButton.setText(_translate("MainWindow", "+"))
        self.zoomFitButton.setText(_translate("MainWindow", "Fit in view"))
        self.zoomOutButton.setText(_translate("MainWindow", "-"))
        self.docCloseButton.setText(_translate("MainWindow", "×"))
        self.captureControlCon.setTitle(_translate("MainWindow", "Capture"))
        self.captureCreateBtn.setText(_translate("MainWindow", "Create"))
        self.captureDelBtn.setText(_translate("MainWindow", "Del"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.settingDockCon.setWindowTitle(_translate("MainWindow", "Setting"))
        self.optionContainer.setTitle(_translate("MainWindow", "Node"))
        self.nodeTabC.setTabText(self.nodeTabC.indexOf(self.nodePreviewTab), _translate("MainWindow", "Preview"))
        self.nodeTabC.setTabText(self.nodeTabC.indexOf(self.nodeOptionC), _translate("MainWindow", "Options"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Captured Items Tree"))
        self.toolButton_2.setText(_translate("MainWindow", "+"))
        self.toolButton_3.setText(_translate("MainWindow", "-"))
        self.controlPanelContainer.setTabText(self.controlPanelContainer.indexOf(self.controlPanelContainerPage1), _translate("MainWindow", "Document Control Panel"))
        self.groupBox.setTitle(_translate("MainWindow", "Opened Docs"))
        self.label_10.setText(_translate("MainWindow", "Project"))
        self.pushButton_2.setText(_translate("MainWindow", "Load"))
        self.pushButton_3.setText(_translate("MainWindow", "Save"))
        self.controlPanelContainer.setTabText(self.controlPanelContainer.indexOf(self.ioTab), _translate("MainWindow", "Opened Docs"))
        self.outputDockCon.setWindowTitle(_translate("MainWindow", "Pipeline"))
        self.pipeRunNodeBtn.setText(_translate("MainWindow", "Run Node"))
        self.pipeRunBtn.setText(_translate("MainWindow", "Run All"))
        self.label_5.setText(_translate("MainWindow", "Capture"))
        self.label_9.setText(_translate("MainWindow", "Pipe"))
        self.PipeAddBtn.setText(_translate("MainWindow", "+"))
        self.PipeUpBtn.setText(_translate("MainWindow", "↑"))
        self.PipeDownBtn.setText(_translate("MainWindow", "↓"))
        self.PipeRemoveBtn.setText(_translate("MainWindow", "-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "PipeNode Option"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Link Edit"))
        self.pipeConfigLoadBtn.setText(_translate("MainWindow", "Load"))
        self.pipeConfigSaveBtn.setText(_translate("MainWindow", "Save"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.pipeEditTab), _translate("MainWindow", "Pipe Edit"))
        self.pipeOptionTabC.setTabText(self.pipeOptionTabC.indexOf(self.pipeOptionTab), _translate("MainWindow", "Pipe Options"))
        self.pipeMemoSelectTabC.setTabText(self.pipeMemoSelectTabC.indexOf(self.pipeDefaultMemoCon), _translate("MainWindow", "Default"))
        self.pipeMemoSelectTabC.setTabText(self.pipeMemoSelectTabC.indexOf(self.pipeCapNodeMemoCon), _translate("MainWindow", "Capture Node"))
        self.pipeOptionTabC.setTabText(self.pipeOptionTabC.indexOf(self.pipeNodeMemoC), _translate("MainWindow", "Node Memo"))
        self.pipeOptionTabC.setTabText(self.pipeOptionTabC.indexOf(self.pipeOutputTab), _translate("MainWindow", "Output"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.pipeNodeEditTab), _translate("MainWindow", "Pipe Node Edit"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
from view.custom_widgets.qcodeeditor import QCodeEditor


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
