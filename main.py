from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import QApplication
from windows.mainWindow import Ui_main_window
from windows.agentCreationWindow import AgentCreationWindow
from settings import Settings
from windows.learningWindow import LearningWindow
import play
from windows import agentDqnDetailsWindow
import windows.informationWindow

class Gui:
    def __init__(self, window, settings: Settings):
        self.ui = Ui_main_window()
        self.main_window=window
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

    def plot(self):
        pixmap = QPixmap('new_curve.png')
        self.ui.curve_view.setPixmap(pixmap)
        self.main_window.repaint()

    def update_infromation_about_episode_number(self,episode_number):
        self.ui.information_label.setText("Trwa uczenie:epizod "+str(episode_number))

    def learning_done(self,episodes,mean_score):

        self.open_information_window(episodes,mean_score)
        self.ui.information_label.setText("Gotowy do uruchomienia")


    def open_information_window(self,episodes,mean_score):
        self.information_window = QtWidgets.QMainWindow()
        self.information_ui = windows.informationWindow.Ui_MainWindow()
        self.information_ui.setupUi(self.information_window)
        self.information_ui.mean_score.setText(str(mean_score))
        self.information_ui.episdes_number.setText( str(episodes))
        self.information_ui.mean_score_label.setText("Średni wynik ze "+str(10)+" ostatnich epizodów" )
        self.information_ui.ok_button.clicked.connect(lambda :self.information_window.close())
        self.information_window.show()

    def accept_start_learning(self):

        self.settigns.game_settings.max_episodes=self.learning_ui.episodes_number.value()
        self.settigns.game_settings.target_accuracy=self.learning_ui.stop_accuracy.value()

        self.game=play.Play(self.settigns)
        self.game.statistics.signal_plot.connect(self.plot)
        self.game.signal_episode.connect(self.update_infromation_about_episode_number)
        self.game.signal_done.connect(self.learning_done)
        self.ui.information_label.setText("Trwa uczenie:epizod 0")
        self.game.start()

        self.learning_window.close()



    def reject_start_learning(self):
        self.learning_window.close()

    def open_agent_creation_window(self):

        self.agent_creation_window = QtWidgets.QMainWindow()
        self.agent_creation_ui = AgentCreationWindow()
        self.agent_creation_ui.setupUi(self.agent_creation_window)
        self.set_current_values_in_agent_creation_form()
        self.agent_creation_ui.confirm_box.accepted.connect(self.accept_new_agent_settings)
        self.agent_creation_ui.confirm_box.rejected.connect(self.reject_new_agent_settings)
        self.agent_creation_ui.default_settings.clicked.connect(self.set_default_agent_details)

        self.agent_creation_window.show()

    def set_current_values_in_agent_creation_form(self):
        self.set_current_algorithm_in_comb_box()
        self.agent_creation_ui.gmma_spin.setValue(self.settigns.agent_settings.gamma)

    def set_current_algorithm_in_comb_box(self):
        index=self.agent_creation_ui.algorithm_slection.findText(settigns.agent_settings.algorithm)
        self.agent_creation_ui.algorithm_slection.setCurrentIndex(index)

    def accept_new_agent_settings(self):
        self.settigns.agent_settings.algorithm=self.agent_creation_ui.algorithm_slection.currentText()
        self.settigns.agent_settings.gamma=self.agent_creation_ui.gmma_spin.value()
        if self.settigns.agent_settings.algorithm=="Deep Q-Learning":
            self.open_dqn_details_windows()
            self.agent_creation_window.close()

    def reject_new_agent_settings(self):
        self.agent_creation_window.close()

    def set_current_values_in_details_windows(self):
        self.agent_details_ui.replay_size_spin.setValue(self.settigns.agent_settings.replay_size)
        self.agent_details_ui.mini_batch_size_zpin.setValue(self.settigns.agent_settings.mini_batch)
        self.agent_details_ui.exploration_decay_spin.setValue(self.settigns.agent_settings.exploration_decay)
        self.agent_details_ui.start_exploration_spin.setValue(self.settigns.agent_settings.start_exploration_value)
        self.agent_details_ui.learning_rate_spin.setValue(self.settigns.agent_settings.learning_rate)
        self.agent_details_ui.mnimal_exploration_spin.setValue( self.settigns.agent_settings.mnimal_exploration)

    def accept_new_agent_details_settings(self):
        self.settigns.agent_settings.replay_size=self.agent_details_ui.replay_size_spin.value()
        self.settigns.agent_settings.mini_batch=self.agent_details_ui.mini_batch_size_zpin.value()
        self.settigns.agent_settings.exploration_decay=self.agent_details_ui.exploration_decay_spin.value()
        self.settigns.agent_settings.start_exploration_value=self.agent_details_ui.start_exploration_spin.value()
        self.settigns.agent_settings.learning_rate=self.agent_details_ui.learning_rate_spin.value()
        self.settigns.agent_settings.mnimal_exploration=self.agent_details_ui.mnimal_exploration_spin.value()
        self.agent_details_window.close()

    def reject_new_agent_details_settings(self):
        self.agent_details_window.close()

    def set_default_agent_details(self):
        if self.settigns.agent_settings.algorithm=="Deep Q-Learning":
            self.settigns.agent_settings.set_dqn_default()
            if not(self.agent_creation_window.isVisible()):
                self.set_current_values_in_details_windows()
            else:
                self.set_current_values_in_agent_creation_form()

    def open_dqn_details_windows(self):
        self.agent_details_window= QtWidgets.QMainWindow()
        self.agent_details_ui = agentDqnDetailsWindow.Ui_MainWindow()
        self.agent_details_ui.setupUi(self.agent_details_window)

        self.agent_details_ui.buttonBox.accepted.connect(self.accept_new_agent_details_settings)
        self.agent_details_ui.buttonBox.rejected.connect(self.reject_new_agent_details_settings)
        self.agent_details_ui.default_settings_button.clicked.connect(self.set_default_agent_details)


        self.set_current_values_in_details_windows()
        self.agent_details_window.show()





if __name__ == "__main__":

    settigns=Settings()
    app = QApplication(sys.argv)
    window=QtWidgets.QMainWindow()
    gui=Gui(window,settigns)
    b=gui.ui.menubar.actions()
    window.show()

    sys.exit(app.exec_())
