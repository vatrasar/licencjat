
from PyQt5 import QtWidgets,QtCore
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QLabel
from mainWindow import Ui_main_window
from agentCreationWindow import AgentCreationWindow
from settings import Settings
from learningWindow import LearningWindow
import play

class Gui:
    def __init__(self, window, settings: Settings):
        self.ui = Ui_main_window()
        self.ui.setupUi(window)
        self.add_actions()
        self.settigns=settigns

    def add_actions(self):
        self.ui.action_create_agent.triggered.connect(self.open_agent_creation_window)
        self.ui.action_learn_settings_open.triggered.connect(self.open_learning_settings_window)


    def open_learning_settings_window(self):
        self.learning_window = QtWidgets.QMainWindow()
        self.learning_ui = LearningWindow()
        self.learning_ui.setupUi(self.learning_window)
        self.learning_ui.confirm_box.accepted.connect(self.accept_start_learning)
        self.learning_ui.confirm_box.rejected.connect(self.reject_start_learning)
        self.learning_window.show()


    def accept_start_learning(self):
        self.game=play.Play(self.settigns)
        self.game.start()


    def reject_start_learning(self):
        self.learning_window.close()

    def open_agent_creation_window(self):

        self.agent_creation_window = QtWidgets.QMainWindow()
        self.agent_creation_ui = AgentCreationWindow()
        self.agent_creation_ui.setupUi(self.agent_creation_window,self.settigns.agent_settings)
        self.agent_creation_ui.confirm_box.accepted.connect(self.accept_new_agent_settings)
        self.agent_creation_ui.confirm_box.rejected.connect(self.reject_new_agent_settings)
        self.agent_creation_window.show()

    def accept_new_agent_settings(self):
        self.settigns.agent_settings.algorithm=self.agent_creation_ui.algorithm_slection.currentText()
        self.agent_creation_window.close()

    def reject_new_agent_settings(self):
        self.agent_creation_window.close()

if __name__ == "__main__":

    settigns=Settings()
    app = QApplication(sys.argv)
    window=QtWidgets.QMainWindow()
    gui=Gui(window,settigns)
    b=gui.ui.menubar.actions()
    window.show()
    sys.exit(app.exec_())
