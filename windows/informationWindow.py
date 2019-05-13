# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'informationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 131)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.episdes_number = QtWidgets.QLabel(self.centralwidget)
        self.episdes_number.setObjectName("episdes_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.episdes_number)
        self.mean_score_label = QtWidgets.QLabel(self.centralwidget)
        self.mean_score_label.setObjectName("mean_score_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.mean_score_label)
        self.mean_score = QtWidgets.QLabel(self.centralwidget)
        self.mean_score.setObjectName("mean_score")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.mean_score)
        self.verticalLayout.addLayout(self.formLayout)
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setObjectName("ok_button")
        self.verticalLayout.addWidget(self.ok_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Podsumowanie nauki"))
        self.label.setText(_translate("MainWindow", "Liczba epizodów:"))
        self.episdes_number.setText(_translate("MainWindow", "TextLabel"))
        self.mean_score_label.setText(_translate("MainWindow", "Średnia dokładność w ostatnich 1000 epizodach "))
        self.mean_score.setText(_translate("MainWindow", "TextLabel"))
        self.ok_button.setText(_translate("MainWindow", "OK"))

