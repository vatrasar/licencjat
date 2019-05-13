# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templatkaTwoorzenieAgenta.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from settings import AgentSettings

class AgentCreationWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 161)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_type = QtWidgets.QLabel(self.centralwidget)
        self.label_type.setObjectName("label_type")
        self.gridLayout.addWidget(self.label_type, 0, 0, 1, 1)
        self.algorithm_slection = QtWidgets.QComboBox(self.centralwidget)
        self.algorithm_slection.setObjectName("algorithm_slection")
        self.algorithm_slection.addItem("")
        self.algorithm_slection.addItem("")
        self.algorithm_slection.addItem("")
        self.algorithm_slection.addItem("")
        self.algorithm_slection.addItem("")
        self.gridLayout.addWidget(self.algorithm_slection, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gmma_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.gmma_spin.setDecimals(3)
        self.gmma_spin.setMinimum(0.01)
        self.gmma_spin.setMaximum(1.0)
        self.gmma_spin.setSingleStep(0.01)
        self.gmma_spin.setObjectName("gmma_spin")
        self.gridLayout.addWidget(self.gmma_spin, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.default_settings = QtWidgets.QPushButton(self.centralwidget)
        self.default_settings.setObjectName("default_settings")
        self.verticalLayout.addWidget(self.default_settings)
        self.confirm_box = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.confirm_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirm_box.setCenterButtons(True)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Tworzenie agenta"))
        self.label_type.setText(_translate("MainWindow", "Typ algorytmu"))
        self.algorithm_slection.setItemText(0, _translate("MainWindow", "Q-Learning"))
        self.algorithm_slection.setItemText(1, _translate("MainWindow", "Deep Q-Learning"))
        self.algorithm_slection.setItemText(2, _translate("MainWindow", "Strategia Gradientowa"))
        self.algorithm_slection.setItemText(3, _translate("MainWindow", "Advantage Actor Critic"))
        self.algorithm_slection.setItemText(4, _translate("MainWindow", "Proximal Policy Optimization"))
        self.label.setText(_translate("MainWindow", "Współczynnnik dyskontowania nagrody"))
        self.default_settings.setText(_translate("MainWindow", "Ustawinia domyślne dla algorytmu"))

