# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templatkaErkanglowny.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setToolTipDuration(-2)
        self.plot = QtWidgets.QWidget(main_window)
        self.plot.setToolTipDuration(5)
        self.plot.setObjectName("plot")
        self.gridLayout = QtWidgets.QGridLayout(self.plot)
        self.gridLayout.setObjectName("gridLayout")
        self.curve_view = QtWidgets.QLabel(self.plot)
        self.curve_view.setText("")
        self.curve_view.setObjectName("curve_view")
        self.gridLayout.addWidget(self.curve_view, 1, 0, 1, 1)
        self.steps_label = QtWidgets.QLabel(self.plot)
        self.steps_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.steps_label.setObjectName("steps_label")
        self.gridLayout.addWidget(self.steps_label, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.information_label = QtWidgets.QLabel(self.plot)
        self.information_label.setMaximumSize(QtCore.QSize(782, 50))
        font = QtGui.QFont()
        font.setFamily("Sarai")
        font.setPointSize(40)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.information_label.setFont(font)
        self.information_label.setAlignment(QtCore.Qt.AlignCenter)
        self.information_label.setObjectName("information_label")
        self.gridLayout.addWidget(self.information_label, 0, 0, 1, 1)
        self.mean_reward_label = QtWidgets.QLabel(self.plot)
        self.mean_reward_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.mean_reward_label.setObjectName("mean_reward_label")
        self.gridLayout.addWidget(self.mean_reward_label, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(self.plot)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        main_window.setCentralWidget(self.plot)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu_agent = QtWidgets.QMenu(self.menubar)
        self.menu_agent.setObjectName("menu_agent")
        self.menu_environment = QtWidgets.QMenu(self.menubar)
        self.menu_environment.setObjectName("menu_environment")
        self.menu_start = QtWidgets.QMenu(self.menubar)
        self.menu_start.setObjectName("menu_start")
        self.menu_graph = QtWidgets.QMenu(self.menubar)
        self.menu_graph.setObjectName("menu_graph")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.action_load_agent = QtWidgets.QAction(main_window)
        self.action_load_agent.setObjectName("action_load_agent")
        self.action_create_agent = QtWidgets.QAction(main_window)
        self.action_create_agent.setObjectName("action_create_agent")
        self.action_agent_edit = QtWidgets.QAction(main_window)
        self.action_agent_edit.setObjectName("action_agent_edit")
        self.actionGry = QtWidgets.QAction(main_window)
        self.actionGry.setObjectName("actionGry")
        self.action_test_settings_open = QtWidgets.QAction(main_window)
        self.action_test_settings_open.setObjectName("action_test_settings_open")
        self.action_learn_settings_open = QtWidgets.QAction(main_window)
        self.action_learn_settings_open.setObjectName("action_learn_settings_open")
        self.action_agent_save = QtWidgets.QAction(main_window)
        self.action_agent_save.setObjectName("action_agent_save")
        self.action_cartpole_prestart = QtWidgets.QAction(main_window)
        self.action_cartpole_prestart.setObjectName("action_cartpole_prestart")
        self.action_pong_prestart = QtWidgets.QAction(main_window)
        self.action_pong_prestart.setObjectName("action_pong_prestart")
        self.action_Sonic_the_hedgehog_prestart = QtWidgets.QAction(main_window)
        self.action_Sonic_the_hedgehog_prestart.setObjectName("action_Sonic_the_hedgehog_prestart")
        self.action_save_graph = QtWidgets.QAction(main_window)
        self.action_save_graph.setObjectName("action_save_graph")
        self.action_game_selection = QtWidgets.QAction(main_window)
        self.action_game_selection.setObjectName("action_game_selection")
        self.menu_agent.addAction(self.action_load_agent)
        self.menu_agent.addAction(self.action_create_agent)
        self.menu_environment.addAction(self.action_game_selection)
        self.menu_start.addAction(self.action_test_settings_open)
        self.menu_start.addAction(self.action_learn_settings_open)
        self.menu_graph.addAction(self.action_save_graph)
        self.menubar.addAction(self.menu_agent.menuAction())
        self.menubar.addAction(self.menu_environment.menuAction())
        self.menubar.addAction(self.menu_start.menuAction())
        self.menubar.addAction(self.menu_graph.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Środowisko do testów algrytmow uczenia ze wzmocnieniem"))
        self.steps_label.setText(_translate("main_window", "Liczba kroków: 0"))
        self.information_label.setText(_translate("main_window", "Gotowy do uruchomienia"))
        self.mean_reward_label.setText(_translate("main_window", "Średnia nagroda: 0"))
        self.label.setText(_translate("main_window", "ostatnia nagroda: 0"))
        self.menu_agent.setTitle(_translate("main_window", "Agent"))
        self.menu_environment.setTitle(_translate("main_window", "Gry"))
        self.menu_start.setTitle(_translate("main_window", "Uruchom"))
        self.menu_graph.setTitle(_translate("main_window", "Wykres"))
        self.action_load_agent.setText(_translate("main_window", "Wczytaj"))
        self.action_create_agent.setText(_translate("main_window", "Stwórz"))
        self.action_agent_edit.setText(_translate("main_window", "Edytuj"))
        self.actionGry.setText(_translate("main_window", "Gry"))
        self.action_test_settings_open.setText(_translate("main_window", "Testy"))
        self.action_learn_settings_open.setText(_translate("main_window", "Nauka"))
        self.action_agent_save.setText(_translate("main_window", "Zapisz"))
        self.action_cartpole_prestart.setText(_translate("main_window", "Cartpole"))
        self.action_pong_prestart.setText(_translate("main_window", "Pong"))
        self.action_Sonic_the_hedgehog_prestart.setText(_translate("main_window", "Sonic the hedgehog"))
        self.action_save_graph.setText(_translate("main_window", "Epizody do średniej"))
        self.action_game_selection.setText(_translate("main_window", "Wybierz"))

