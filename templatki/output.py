# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PPODetails.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(443, 220)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.epslion_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.epslion_spin.setDecimals(3)
        self.epslion_spin.setMinimum(0.0)
        self.epslion_spin.setMaximum(1.0)
        self.epslion_spin.setObjectName("epslion_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.epslion_spin)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.c2_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.c2_spin.setDecimals(3)
        self.c2_spin.setMaximum(1.0)
        self.c2_spin.setSingleStep(0.001)
        self.c2_spin.setObjectName("c2_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.c2_spin)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setMaximum(1.0)
        self.doubleSpinBox.setSingleStep(0.001)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.default_settings_button = QtWidgets.QPushButton(self.centralwidget)
        self.default_settings_button.setObjectName("default_settings_button")
        self.verticalLayout.addWidget(self.default_settings_button)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "A2C szczegóły"))
        self.label_2.setText(_translate("MainWindow", "epslion (z funkcji  clip)"))
        self.label.setText(_translate("MainWindow", "c2 (współczynnik entropi)"))
        self.label_3.setText(_translate("MainWindow", "c1 (współczynnik krytyka)"))
        self.default_settings_button.setText(_translate("MainWindow", "Ustawnienia domyslne dla algorytmu"))

