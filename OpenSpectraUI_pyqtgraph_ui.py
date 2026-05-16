# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OpenSpectraUI_pyqtgraph.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(320, -10, 151, 41))
        font = QFont()
        font.setPointSize(18)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(Qt.PlainText)
        self.set_laser = QPushButton(self.centralwidget)
        self.set_laser.setObjectName(u"set_laser")
        self.set_laser.setGeometry(QRect(700, 240, 91, 34))
        self.set_led = QPushButton(self.centralwidget)
        self.set_led.setObjectName(u"set_led")
        self.set_led.setGeometry(QRect(700, 290, 91, 34))
        self.save_btn = QPushButton(self.centralwidget)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setGeometry(QRect(700, 360, 91, 34))
        self.graphwidget = PlotWidget(self.centralwidget)
        self.graphwidget.setObjectName(u"graphwidget")
        self.graphwidget.setGeometry(QRect(30, 110, 661, 411))
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 40, 233, 51))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.selectPort = QComboBox(self.gridLayoutWidget)
        self.selectPort.setObjectName(u"selectPort")

        self.gridLayout.addWidget(self.selectPort, 2, 0, 1, 1)

        self.Connect = QPushButton(self.gridLayoutWidget)
        self.Connect.setObjectName(u"Connect")

        self.gridLayout.addWidget(self.Connect, 2, 1, 1, 1)

        self.label_port = QLabel(self.gridLayoutWidget)
        self.label_port.setObjectName(u"label_port")

        self.gridLayout.addWidget(self.label_port, 1, 0, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(320, 70, 160, 26))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Run = QPushButton(self.horizontalLayoutWidget)
        self.Run.setObjectName(u"Run")

        self.horizontalLayout.addWidget(self.Run)

        self.Pause = QPushButton(self.horizontalLayoutWidget)
        self.Pause.setObjectName(u"Pause")

        self.horizontalLayout.addWidget(self.Pause)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(530, 70, 261, 26))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_int_time = QLabel(self.horizontalLayoutWidget_2)
        self.label_int_time.setObjectName(u"label_int_time")

        self.horizontalLayout_2.addWidget(self.label_int_time)

        self.int_time = QLineEdit(self.horizontalLayoutWidget_2)
        self.int_time.setObjectName(u"int_time")

        self.horizontalLayout_2.addWidget(self.int_time)

        self.set_int_time = QPushButton(self.horizontalLayoutWidget_2)
        self.set_int_time.setObjectName(u"set_int_time")

        self.horizontalLayout_2.addWidget(self.set_int_time)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"Open Spectra", None))
        self.set_laser.setText(QCoreApplication.translate("MainWindow", u"UV  LASER", None))
        self.set_led.setText(QCoreApplication.translate("MainWindow", u"WHITE LED", None))
        self.save_btn.setText(QCoreApplication.translate("MainWindow", u"SAVE", None))
        self.Connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label_port.setText(QCoreApplication.translate("MainWindow", u"COM Port:", None))
        self.Run.setText(QCoreApplication.translate("MainWindow", u"RUN", None))
        self.Pause.setText(QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.label_int_time.setText(QCoreApplication.translate("MainWindow", u"Integration time (us)", None))
        self.int_time.setText(QCoreApplication.translate("MainWindow", u"1000000", None))
        self.set_int_time.setText(QCoreApplication.translate("MainWindow", u"SET", None))
    # retranslateUi

