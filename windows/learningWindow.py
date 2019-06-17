# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets

class LearningWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(408, 190)
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
        self.steps_number = QtWidgets.QSpinBox(self.centralwidget)
        self.steps_number.setMinimum(1)
        self.steps_number.setMaximum(990000000)
        self.steps_number.setObjectName("steps_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.steps_number)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.stop_accuracy = QtWidgets.QSpinBox(self.centralwidget)
        self.stop_accuracy.setMinimum(-999999)
        self.stop_accuracy.setMaximum(999999999)
        self.stop_accuracy.setObjectName("stop_accuracy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.stop_accuracy)
        self.saved_agent_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.saved_agent_radio.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.saved_agent_radio.setText("")
        self.saved_agent_radio.setObjectName("saved_agent_radio")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.saved_agent_radio)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.new_agent_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.new_agent_radio.setText("")
        self.new_agent_radio.setObjectName("new_agent_radio")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.new_agent_radio)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.Is_LSTM_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.Is_LSTM_checkbox.setText("")
        self.Is_LSTM_checkbox.setObjectName("Is_LSTM_checkbox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Is_LSTM_checkbox)
        self.verticalLayout.addLayout(self.formLayout)
        self.confirm_box = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.confirm_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.confirm_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirm_box.setObjectName("confirm_box")
        self.verticalLayout.addWidget(self.confirm_box, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ustawienia treningu"))
        self.label.setText(_translate("MainWindow", "Maksymalna liczba ruchów"))
        self.label_2.setText(_translate("MainWindow", "Zatrzymaj gdy średniu wynik"))
        self.stop_accuracy.setSuffix(_translate("MainWindow", " pkt"))
        self.label_3.setText(_translate("MainWindow", "Uzyj wczytanego agenta"))
        self.label_4.setText(_translate("MainWindow", "Uzyj nowego agenta"))
        self.label_5.setText(_translate("MainWindow", "Sieci LSTM"))





