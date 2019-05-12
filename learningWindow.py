# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templatkaUruchamianieui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import pylab
from PyQt5 import QtCore, QtGui, QtWidgets

class LearningWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(378, 131)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, -1, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.episodes_number = QtWidgets.QSpinBox(self.centralwidget)
        self.episodes_number.setMinimum(1)
        self.episodes_number.setMaximum(30000000)
        self.episodes_number.setObjectName("episodes_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.episodes_number)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.stop_accuracy = QtWidgets.QSpinBox(self.centralwidget)
        self.stop_accuracy.setMaximum(100)
        self.stop_accuracy.setObjectName("stop_accuracy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.stop_accuracy)
        self.verticalLayout.addLayout(self.formLayout)
        self.confirm_box = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.confirm_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirm_box.setObjectName("confirm_box")
        self.verticalLayout.addWidget(self.confirm_box)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ustawienia treningu"))
        self.label.setText(_translate("MainWindow", "Liczba epizdow"))
        self.label_2.setText(_translate("MainWindow", "Zatrzymaj po osiągnieciu dokładności"))
        self.stop_accuracy.setSuffix(_translate("MainWindow", "%"))

