
from PyQt5 import QtWidgets,QtCore
import sys
from PyQt5.QtWidgets import QApplication,QDialog,QLabel
from mainWindow import Ui_main_window
from agentCreationWindow import AgentCreationWindow
class Gui:
    def __init__(self,window):
        self.ui = Ui_main_window()
        self.ui.setupUi(window)
        self.add_actions()

    def add_actions(self):
        self.ui.action_create_agent.triggered.connect(self.open_agent_creation_window)

    def open_agent_creation_window(self):

        self.agent_creation_window = QtWidgets.QMainWindow()
        self.agent_creation_ui = AgentCreationWindow()
        self.agent_creation_ui.setupUi(self.agent_creation_window)
        self.agent_creation_ui.confirm_box.accepted.connect(self.accept_new_agent_settings)
        self.agent_creation_ui.confirm_box.rejected.connect(self.reject_new_agent_settings)
        self.agent_creation_window.show()
    def accept_new_agent_settings(self):
        pass
    def reject_new_agent_settings(self):
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window=QtWidgets.QMainWindow()
    gui=Gui(window)
    b=gui.ui.menubar.actions()
    window.show()
    sys.exit(app.exec_())
