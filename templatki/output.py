# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DQNSzczegolyTemplatkaNowa.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(462, 259)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.replay_size_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.replay_size_spin.setMinimum(10)
        self.replay_size_spin.setMaximum(9999999)
        self.replay_size_spin.setObjectName("replay_size_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.replay_size_spin)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.mini_batch_size_zpin = QtWidgets.QSpinBox(self.centralwidget)
        self.mini_batch_size_zpin.setMinimum(1)
        self.mini_batch_size_zpin.setMaximum(9999999)
        self.mini_batch_size_zpin.setObjectName("mini_batch_size_zpin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.mini_batch_size_zpin)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.learning_rate_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.learning_rate_spin.setDecimals(3)
        self.learning_rate_spin.setMinimum(0.0)
        self.learning_rate_spin.setMaximum(1.0)
        self.learning_rate_spin.setObjectName("learning_rate_spin")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.learning_rate_spin)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.exploration_decay_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.exploration_decay_spin.setDecimals(5)
        self.exploration_decay_spin.setMaximum(0.99)
        self.exploration_decay_spin.setObjectName("exploration_decay_spin")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.exploration_decay_spin)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.mnimal_exploration_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.mnimal_exploration_spin.setDecimals(5)
        self.mnimal_exploration_spin.setMaximum(0.99)
        self.mnimal_exploration_spin.setObjectName("mnimal_exploration_spin")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.mnimal_exploration_spin)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "DQN szczegóły"))
        self.label.setText(_translate("MainWindow", "Wilkość bufora replay"))
        self.replay_size_spin.setSuffix(_translate("MainWindow", " ruchów"))
        self.label_6.setText(_translate("MainWindow", "Wielkość partii do nauki"))
        self.label_2.setText(_translate("MainWindow", "Współczynnik uczenia"))
        self.label_4.setText(_translate("MainWindow", "Fragment teningu w którym jest eksploracja"))
        self.label_5.setText(_translate("MainWindow", "Mnimalny poziom eksploracji"))
        self.default_settings_button.setText(_translate("MainWindow", "Ustawnienia domyslne dla algorytmu"))

