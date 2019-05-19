# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'A2CSzczegolyTemplatka.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(425, 176)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.actor_learning_rate_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.actor_learning_rate_spin.setDecimals(3)
        self.actor_learning_rate_spin.setMinimum(0.0)
        self.actor_learning_rate_spin.setMaximum(1.0)
        self.actor_learning_rate_spin.setObjectName("actor_learning_rate_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.actor_learning_rate_spin)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.critic_learning_rate_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.critic_learning_rate_spin.setDecimals(3)
        self.critic_learning_rate_spin.setMaximum(1.0)
        self.critic_learning_rate_spin.setSingleStep(0.001)
        self.critic_learning_rate_spin.setObjectName("critic_learning_rate_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.critic_learning_rate_spin)
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
        self.label_2.setText(_translate("MainWindow", "Współczynnik uczenia aktora"))
        self.label.setText(_translate("MainWindow", "Współczynnik uczenia krytyka"))
        self.default_settings_button.setText(_translate("MainWindow", "Ustawnienia domyslne dla algorytmu"))

