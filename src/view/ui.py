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
        self.gridLayout_21 = QtWidgets.QGridLayout(self.previewControlContainer)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.previewControlContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_7.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.toolButton_7 = QtWidgets.QToolButton(parent=self.groupBox_4)
        self.toolButton_7.setCheckable(True)
        self.toolButton_7.setObjectName("toolButton_7")
        self.horizontalLayout_7.addWidget(self.toolButton_7)
        self.toolButton_6 = QtWidgets.QToolButton(parent=self.groupBox_4)
        self.toolButton_6.setCheckable(True)
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout_7.addWidget(self.toolButton_6)
        self.toolButton_4 = QtWidgets.QToolButton(parent=self.groupBox_4)
        self.toolButton_4.setCheckable(True)
        self.toolButton_4.setArrowType(QtCore.Qt.ArrowType.NoArrow)
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout_7.addWidget(self.toolButton_4)
        self.toolButton_8 = QtWidgets.QToolButton(parent=self.groupBox_4)
        self.toolButton_8.setCheckable(True)
        self.toolButton_8.setObjectName("toolButton_8")
        self.horizontalLayout_7.addWidget(self.toolButton_8)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.toolButton_5 = QtWidgets.QToolButton(parent=self.groupBox_4)
        self.toolButton_5.setAutoRaise(False)
        self.toolButton_5.setObjectName("toolButton_5")
        self.horizontalLayout_7.addWidget(self.toolButton_5)
        self.toolButton_5.raise_()
        self.toolButton_6.raise_()
        self.toolButton_4.raise_()
        self.toolButton_8.raise_()
        self.toolButton_7.raise_()
        self.gridLayout_21.addWidget(self.groupBox_4, 2, 0, 1, 1)
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
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.docCloseButton = QtWidgets.QToolButton(parent=self.horizontalGroupBox_2)
        self.docCloseButton.setObjectName("docCloseButton")
        self.horizontalLayout_4.addWidget(self.docCloseButton)
        self.gridLayout_21.addWidget(self.horizontalGroupBox_2, 1, 0, 1, 1)
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
        self.tabWidget = QtWidgets.QTabWidget(parent=self.ioTab)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_10 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_10.sizePolicy().hasHeightForWidth())
        self.tab_10.setSizePolicy(sizePolicy)
        self.tab_10.setObjectName("tab_10")
        self.tabWidget.addTab(self.tab_10, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.tab_8)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.label_8 = QtWidgets.QLabel(parent=self.tab_8)
        self.label_8.setObjectName("label_8")
        self.gridLayout_20.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.tab_8)
        self.label_6.setObjectName("label_6")
        self.gridLayout_20.addWidget(self.label_6, 0, 0, 1, 1)
        self.downloadURLInput = QtWidgets.QLineEdit(parent=self.tab_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadURLInput.sizePolicy().hasHeightForWidth())
        self.downloadURLInput.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.downloadURLInput.setFont(font)
        self.downloadURLInput.setFrame(True)
        self.downloadURLInput.setObjectName("downloadURLInput")
        self.gridLayout_20.addWidget(self.downloadURLInput, 0, 1, 1, 1)
        self.downloadConfirmButton = QtWidgets.QToolButton(parent=self.tab_8)
        self.downloadConfirmButton.setObjectName("downloadConfirmButton")
        self.gridLayout_20.addWidget(self.downloadConfirmButton, 0, 2, 1, 1)
        self.downloadProgressBar = QtWidgets.QProgressBar(parent=self.tab_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadProgressBar.sizePolicy().hasHeightForWidth())
        self.downloadProgressBar.setSizePolicy(sizePolicy)
        self.downloadProgressBar.setProperty("value", 0)
        self.downloadProgressBar.setObjectName("downloadProgressBar")
        self.gridLayout_20.addWidget(self.downloadProgressBar, 1, 1, 1, 2)
        self.tabWidget.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.tabWidget.addTab(self.tab_9, "")
        self.verticalLayout_10.addWidget(self.tabWidget)
        self.groupBox_21 = QtWidgets.QGroupBox(parent=self.ioTab)
        self.groupBox_21.setObjectName("groupBox_21")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_21)
        self.horizontalLayout_8.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_21)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.pdfLoadingProgress = QtWidgets.QProgressBar(parent=self.groupBox_21)
        self.pdfLoadingProgress.setProperty("value", 0)
        self.pdfLoadingProgress.setObjectName("pdfLoadingProgress")
        self.horizontalLayout_8.addWidget(self.pdfLoadingProgress)
        self.verticalLayout_10.addWidget(self.groupBox_21)
        self.openedDocList = QtWidgets.QListView(parent=self.ioTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.openedDocList.sizePolicy().hasHeightForWidth())
        self.openedDocList.setSizePolicy(sizePolicy)
        self.openedDocList.setObjectName("openedDocList")
        self.verticalLayout_10.addWidget(self.openedDocList)
        self.groupBox_22 = QtWidgets.QGroupBox(parent=self.ioTab)
        self.groupBox_22.setObjectName("groupBox_22")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_22)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(parent=self.groupBox_22)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.groupBox_22)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.groupBox_22)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout_10.addWidget(self.groupBox_22)
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
        self.pipeProgress = QtWidgets.QProgressBar(parent=self.dockWidgetContents_6)
        self.pipeProgress.setProperty("value", 24)
        self.pipeProgress.setObjectName("pipeProgress")
        self.gridLayout_22.addWidget(self.pipeProgress, 3, 0, 1, 1)
        self.pipeOptionTabC = QtWidgets.QTabWidget(parent=self.dockWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.pipeOptionTabC.sizePolicy().hasHeightForWidth())
        self.pipeOptionTabC.setSizePolicy(sizePolicy)
        self.pipeOptionTabC.setObjectName("pipeOptionTabC")
        self.pipeOptionTab = QtWidgets.QWidget()
        self.pipeOptionTab.setObjectName("pipeOptionTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pipeOptionTab)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pipeOptionContainer = QtWidgets.QGroupBox(parent=self.pipeOptionTab)
        self.pipeOptionContainer.setTitle("")
        self.pipeOptionContainer.setObjectName("pipeOptionContainer")
        self.verticalLayout_2.addWidget(self.pipeOptionContainer)
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
        self.gridLayout_22.addWidget(self.pipeOptionTabC, 1, 0, 1, 1)
        self.pipeRunBtn = QtWidgets.QPushButton(parent=self.dockWidgetContents_6)
        self.pipeRunBtn.setObjectName("pipeRunBtn")
        self.gridLayout_22.addWidget(self.pipeRunBtn, 4, 0, 1, 1)
        self.pipeNodeProgress = QtWidgets.QProgressBar(parent=self.dockWidgetContents_6)
        self.pipeNodeProgress.setProperty("value", 24)
        self.pipeNodeProgress.setObjectName("pipeNodeProgress")
        self.gridLayout_22.addWidget(self.pipeNodeProgress, 2, 0, 1, 1)
        self.groupBox_23 = QtWidgets.QGroupBox(parent=self.dockWidgetContents_6)
        self.groupBox_23.setObjectName("groupBox_23")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_23)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pipeAvaliableCombo = QtWidgets.QComboBox(parent=self.groupBox_23)
        self.pipeAvaliableCombo.setObjectName("pipeAvaliableCombo")
        self.verticalLayout_4.addWidget(self.pipeAvaliableCombo)
        self.widget = QtWidgets.QWidget(parent=self.groupBox_23)
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
        self.pipelineList = QtWidgets.QListWidget(parent=self.groupBox_23)
        self.pipelineList.setObjectName("pipelineList")
        self.verticalLayout_4.addWidget(self.pipelineList)
        self.widget_2 = QtWidgets.QWidget(parent=self.groupBox_23)
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
        self.gridLayout_22.addWidget(self.groupBox_23, 0, 0, 1, 1)
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
        self.controlPanelContainer.setCurrentIndex(0)
        self.nodeTabC.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.pipeOptionTabC.setCurrentIndex(1)
        self.pipeMemoSelectTabC.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.previewContainer.setTitle(_translate("MainWindow", "Preview"))
        self.previewImageContainer.setTitle(_translate("MainWindow", "Preview"))
        self.previewControlContainer.setTitle(_translate("MainWindow", "Control"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Capture"))
        self.toolButton_7.setText(_translate("MainWindow", "Drag"))
        self.toolButton_6.setText(_translate("MainWindow", "Text"))
        self.toolButton_4.setText(_translate("MainWindow", "Image"))
        self.toolButton_8.setText(_translate("MainWindow", "Formula"))
        self.toolButton_5.setText(_translate("MainWindow", "Del"))
        self.horizontalGroupBox_2.setTitle(_translate("MainWindow", "Doc Control"))
        self.previewPrevButton.setText(_translate("MainWindow", "<"))
        self.previewNextButton.setText(_translate("MainWindow", ">"))
        self.label_11.setText(_translate("MainWindow", "Zoom:"))
        self.zoomInButton.setText(_translate("MainWindow", "+"))
        self.zoomFitButton.setText(_translate("MainWindow", "Fit in view"))
        self.zoomOutButton.setText(_translate("MainWindow", "-"))
        self.docCloseButton.setText(_translate("MainWindow", "×"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.settingDockCon.setWindowTitle(_translate("MainWindow", "Setting"))
        self.optionContainer.setTitle(_translate("MainWindow", "Node"))
        self.nodeTabC.setTabText(self.nodeTabC.indexOf(self.nodePreviewTab), _translate("MainWindow", "Preview"))
        self.nodeTabC.setTabText(self.nodeTabC.indexOf(self.nodeOptionC), _translate("MainWindow", "Options"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Captured Items Tree"))
        self.toolButton_2.setText(_translate("MainWindow", "+"))
        self.toolButton_3.setText(_translate("MainWindow", "-"))
        self.controlPanelContainer.setTabText(self.controlPanelContainer.indexOf(self.controlPanelContainerPage1), _translate("MainWindow", "Document Control Panel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), _translate("MainWindow", "Open"))
        self.label_8.setText(_translate("MainWindow", "Download:"))
        self.label_6.setText(_translate("MainWindow", "From URL"))
        self.downloadConfirmButton.setText(_translate("MainWindow", "✔︎"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("MainWindow", "Download"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), _translate("MainWindow", "From Publisher"))
        self.groupBox_21.setTitle(_translate("MainWindow", "Status"))
        self.label_7.setText(_translate("MainWindow", "PDF loading:"))
        self.label_10.setText(_translate("MainWindow", "Project"))
        self.pushButton_2.setText(_translate("MainWindow", "Load"))
        self.pushButton_3.setText(_translate("MainWindow", "Save"))
        self.controlPanelContainer.setTabText(self.controlPanelContainer.indexOf(self.ioTab), _translate("MainWindow", "Opened Docs"))
        self.outputDockCon.setWindowTitle(_translate("MainWindow", "Pipeline"))
        self.pipeOptionTabC.setTabText(self.pipeOptionTabC.indexOf(self.pipeOptionTab), _translate("MainWindow", "Pipe Options"))
        self.pipeMemoSelectTabC.setTabText(self.pipeMemoSelectTabC.indexOf(self.pipeDefaultMemoCon), _translate("MainWindow", "Default"))
        self.pipeMemoSelectTabC.setTabText(self.pipeMemoSelectTabC.indexOf(self.pipeCapNodeMemoCon), _translate("MainWindow", "Capture Node"))
        self.pipeOptionTabC.setTabText(self.pipeOptionTabC.indexOf(self.pipeNodeMemoC), _translate("MainWindow", "Node Memo"))
        self.pipeOptionTabC.setTabText(self.pipeOptionTabC.indexOf(self.pipeOutputTab), _translate("MainWindow", "Output"))
        self.pipeRunBtn.setText(_translate("MainWindow", "Run"))
        self.groupBox_23.setTitle(_translate("MainWindow", "Pipe Editor"))
        self.PipeAddBtn.setText(_translate("MainWindow", "+"))
        self.PipeUpBtn.setText(_translate("MainWindow", "↑"))
        self.PipeDownBtn.setText(_translate("MainWindow", "↓"))
        self.PipeRemoveBtn.setText(_translate("MainWindow", "-"))
        self.pipeConfigLoadBtn.setText(_translate("MainWindow", "Load"))
        self.pipeConfigSaveBtn.setText(_translate("MainWindow", "Save"))
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
