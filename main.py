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
import windows.gameSelection
import windows.testWindow
import windows.PGSettingsWindow
import windows.agentA2cDetails
import windows.agentPPODetails
import windows.alterWindow
from PyQt5.QtWidgets import  QFileDialog


class Gui:
    def __init__(self, window, settings: Settings):
        self.ui = Ui_main_window()
        self.main_window=window
        self.ui.setupUi(window)
        self.add_actions()
        self.settigns=settigns
        self.loaded_agent_directory=""

    def add_actions(self):
        self.ui.action_create_agent.triggered.connect(self.open_agent_creation_window)
        self.ui.action_learn_settings_open.triggered.connect(self.open_learning_settings_window)
        self.ui.action_game_selection.triggered.connect(self.open_game_selection_window)
        self.ui.action_test_settings_open.triggered.connect(self.open_test_settings_window)
        self.ui.action_load_agent.triggered.connect(self.open_load_agent_dialog)

    def open_load_agent_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.loaded_agent_directory=fileName



    def open_test_settings_window(self):
        self.test_settings_window = QtWidgets.QMainWindow()
        self.test_settings_ui = windows.testWindow.Ui_MainWindow()
        self.test_settings_ui.setupUi(self.test_settings_window)
        self.test_settings_ui.buttonBox.accepted.connect(self.accept_test_settings)
        self.test_settings_ui.buttonBox.rejected.connect(self.reject_test_settings)

        self.test_settings_window.show()

    def reject_test_settings(self):
        self.test_settings_window.close()

    def accept_test_settings(self):
        self.settigns.game_settings.max_episodes = self.test_settings_ui.spinBox.value()

        self.settigns.agent_settings.start_exploration_value=0.001

        self.test_settings_window.close()
        if self.test_settings_ui.saved_agent_radio.isChecked() and self.settigns.game_settings.game_name != self.get_orginal_game_name_fro_agent(
                self.loaded_agent_directory):
            self.open_alter_windows("Uwaga! Agent mógł być trenowany na grze innej niż jest obecnie ustawiona!",True)
        else:

            self.prepare_tests()



    def open_game_selection_window(self):
        self.game_selection_window = QtWidgets.QMainWindow()
        self.game_selection_ui = windows.gameSelection.Ui_MainWindow()
        self.game_selection_ui.setupUi(self.game_selection_window)
        self.game_selection_ui.buttonBox.accepted.connect(self.accept_selected_game)
        self.game_selection_ui.buttonBox.rejected.connect(self.reject_selected_game)
        self.set_current_game_comb_box()
        self.game_selection_window.show()

    def accept_selected_game(self):
        self.settigns.game_settings.game_name=self.game_selection_ui.game_combo_box.currentText()
        self.game_selection_window.close()

    def reject_selected_game(self):

        self.game_selection_window.close()


    def set_current_game_comb_box(self):
        index = self.game_selection_ui.game_combo_box.findText(settigns.game_settings.game_name)
        self.game_selection_ui.game_combo_box.setCurrentIndex(index)

    def open_learning_settings_window(self):
        self.learning_window = QtWidgets.QMainWindow()
        self.learning_ui = LearningWindow()
        self.learning_ui.setupUi(self.learning_window)
        self.learning_ui.confirm_box.accepted.connect(self.accept_start_learning)
        self.learning_ui.confirm_box.rejected.connect(self.reject_start_learning)
        if self.loaded_agent_directory=="":
            self.learning_ui.saved_agent_radio.setCheckable(False)
        else:
            self.learning_ui.saved_agent_radio.setCheckable(True)
        self.learning_window.show()

    def set_current_algorithm_in_comb_box(self):
        index = self.agent_creation_ui.algorithm_slection.findText(settigns.agent_settings.algorithm)
        self.agent_creation_ui.algorithm_slection.setCurrentIndex(index)

    def plot(self):
        pixmap = QPixmap('new_curve.png')
        self.ui.curve_view.setPixmap(pixmap)
        self.main_window.repaint()

    def update_infromation_about_episode_number(self,episode_number):
        self.ui.information_label.setText("Trwa uczenie:epizod "+str(episode_number))

    def update_infromation_about_episode_number_in_test(self,episode_number):
        self.ui.information_label.setText("Trwa testowanie:epizod "+str(episode_number))

    def learning_done(self,episodes,mean_score):

        self.open_information_window(episodes,mean_score)
        self.ui.information_label.setText("Gotowy do uruchomienia")

    def test_done(self,episodes,mean_score):

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


        if self.learning_ui.saved_agent_radio.isChecked() and self.settigns.game_settings.game_name!=self.get_orginal_game_name_fro_agent(self.loaded_agent_directory):
            self.open_alter_windows("Uwaga! Agent mógł być trenowany na grze innej niż jest obecnie ustawiona!")


        else:

            self.prepare_learning()

        self.learning_window.close()

    def prepare_learning(self):

        self.settigns.game_settings.max_steps_number = self.learning_ui.steps_number.value()

        self.settigns.game_settings.target_accuracy = self.learning_ui.stop_accuracy.value()

        if self.settigns.game_settings.game_name == "cartpole":
            self.game = play.Play(self.settigns, False, False, self.loaded_agent_directory,
                                  self.learning_ui.saved_agent_radio.isChecked())
        if self.settigns.game_settings.game_name == "Pong":
            self.game = play.PlayPong(self.settigns, False, False, self.loaded_agent_directory,
                                      self.learning_ui.saved_agent_radio.isChecked())

        self.game.statistics.signal_plot.connect(self.plot)
        self.game.signal_episode.connect(self.update_infromation_about_episode_number)
        self.game.signal_done.connect(self.learning_done)


        self.ui.information_label.setText("Trwa uczenie:epizod 0")

        self.game.start()

    def prepare_tests(self):

        self.settigns.game_settings.max_episodes = self.test_settings_ui.spinBox.value()

        if self.test_settings_ui.saved_agent_radio.isChecked():
            loaded_agent_directory=self.loaded_agent_directory
        else:
            loaded_agent_directory=""

        if self.settigns.game_settings.game_name == "cartpole":

            self.game = play.Play(self.settigns, True, True, loaded_agent_directory,
                                  True)
        if self.settigns.game_settings.game_name == "Pong":
            self.game = play.PlayPong(self.settigns,True, True,loaded_agent_directory,
                                      True)

        self.game.statistics.signal_plot.connect(self.plot)
        self.game.signal_episode.connect(self.update_infromation_about_episode_number)
        self.game.signal_done.connect(self.learning_done)


        self.ui.information_label.setText("Testy:epizod 0")


        self.game.start()


    def open_alter_windows(self, aleter_text,is_test):

        self.alter_window = QtWidgets.QMainWindow()
        self.alter_ui = windows.alterWindow.Ui_MainWindow()
        self.alter_ui.setupUi(self.alter_window)
        self.alter_ui.alter.setText(aleter_text)
        if is_test:
            self.alter_ui.buttonBox.accepted.connect(self.accept_test_action)
        else:
            self.alter_ui.buttonBox.accepted.connect(self.accept_learning_action)
        self.alter_ui.buttonBox.rejected.connect(self.reject_action)


        self.alter_window.show()
    def accept_test_action(self):
        self.prepare_learning()
        self.alter_window.close()
    def accept_learning_action(self):
        self.prepare_learning()
        self.alter_window.close()
    def reject_action(self):
        self.alter_window.close()
    def get_orginal_game_name_fro_agent(self,agent_directory):
        input=open(agent_directory[0:-4]+".txt","r")
        game_name=input.readline()
        input.close()
        return game_name
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
        if self.settigns.agent_settings.algorithm=="Strategia Gradientowa":
            self.open_pg_details_windows()
        if self.settigns.agent_settings.algorithm == "Advantage Actor Critic":
            self.open_a2c_details_windows()
        if self.settigns.agent_settings.algorithm == "Proximal Policy Optimization":
            self.open_ppo_details_windows()


        self.agent_creation_window.close()

    def open_ppo_details_windows(self):
        self.agent_ppo_details_window = QtWidgets.QMainWindow()
        self.agent_ppo_details_ui = windows.agentPPODetails.Ui_MainWindow()
        self.agent_ppo_details_ui.setupUi(self.agent_ppo_details_window)

        self.agent_ppo_details_ui.buttonBox.accepted.connect(self.accept_new_agent_ppo_details_settings)
        self.agent_ppo_details_ui.buttonBox.rejected.connect(self.reject_new_agent_ppo_details_settings)
        self.agent_ppo_details_ui.default_settings_button.clicked.connect(self.set_default_agent_ppo_details)
        self.agent_ppo_details_ui.c2_spin.setValue(settigns.agent_settings.c2)
        self.agent_ppo_details_ui.c1_spin.setValue(settigns.agent_settings.c1)
        self.agent_ppo_details_ui.epslion_spin.setValue(settigns.agent_settings.clip_epslion)

        self.agent_ppo_details_window.show()



    def set_default_agent_ppo_details(self):
        if settigns.game_settings.game_name == "cartpole":
            self.settigns.agent_settings.set_ppo_cartpole_default()
        if settigns.game_settings.game_name == "Pong":
            self.settigns.agent_settings.set_ppo_pong_default()
        self.agent_ppo_details_ui.c2_spin.setValue(settigns.agent_settings.c2)
        self.agent_ppo_details_ui.c1_spin.setValue(settigns.agent_settings.c1)
        self.agent_ppo_details_ui.epslion_spin.setValue(settigns.agent_settings.clip_epslion)

    def accept_new_agent_ppo_details_settings(self):
        settigns.agent_settings.c2=self.agent_ppo_details_ui.c2_spin.value()
        settigns.agent_settings.c1=self.agent_ppo_details_ui.c1_spin.value()
        settigns.agent_settings.clip_epslion=self.agent_ppo_details_ui.epslion_spin.value()
        self.agent_ppo_details_window.close()

    def reject_new_agent_ppo_details_settings(self):
        self.agent_ppo_details_window.close()

    def open_a2c_details_windows(self):

        self.agent_a2c_details_window = QtWidgets.QMainWindow()
        self.agent_a2c_details_ui = windows.agentA2cDetails.Ui_MainWindow()
        self.agent_a2c_details_ui.setupUi(self.agent_a2c_details_window)

        self.agent_a2c_details_ui.buttonBox.accepted.connect(self.accept_new_agent_a2c_details_settings)
        self.agent_a2c_details_ui.buttonBox.rejected.connect(self.reject_new_agent_a2c_details_settings)
        self.agent_a2c_details_ui.default_settings_button.clicked.connect(self.set_default_agent_a2c_details)
        self.agent_a2c_details_ui.actor_learning_rate_spin.setValue(settigns.agent_settings.actor_lr)
        self.agent_a2c_details_ui.critic_learning_rate_spin.setValue(settigns.agent_settings.critic_lr)

        self.agent_a2c_details_window.show()

    def accept_new_agent_a2c_details_settings(self):
        self.settigns.agent_settings.actor_lr=self.agent_a2c_details_ui.actor_learning_rate_spin.value()
        self.settigns.agent_settings.critic_lr=self.agent_a2c_details_ui.critic_learning_rate_spin.value()
        self.agent_a2c_details_window.close()


    def reject_new_agent_a2c_details_settings(self):
        self.agent_a2c_details_window.close()

    def set_default_agent_a2c_details(self):
        self.settigns.agent_settings.set_a2c_cartpole_default()
        self.agent_a2c_details_ui.actor_learning_rate_spin.setValue(settigns.agent_settings.actor_lr)
        self.agent_a2c_details_ui.critic_learning_rate_spin.setValue(settigns.agent_settings.critic_lr)


    def open_pg_details_windows(self):

        self.agent_pg_details_window = QtWidgets.QMainWindow()
        self.agent_pg_details_ui = windows.PGSettingsWindow.Ui_MainWindow()
        self.agent_pg_details_ui.setupUi(self.agent_pg_details_window)

        self.agent_pg_details_ui.buttonBox.accepted.connect(self.accept_new_agent_pg_details_settings)
        self.agent_pg_details_ui.buttonBox.rejected.connect(self.reject_new_agent_pg_details_settings)
        self.agent_pg_details_ui.default_settings_button.clicked.connect(self.set_default_agent_pg_details)


        self.agent_pg_details_window.show()

    def accept_new_agent_pg_details_settings(self):
        self.settigns.agent_settings.learning_rate = self.agent_pg_details_ui.learning_rate_spin.value()
        self.agent_pg_details_window.close()

    def reject_new_agent_pg_details_settings(self):

        self.agent_pg_details_window.close()
    def set_default_agent_pg_details(self):
        self.agent_pg_details_ui.learning_rate_spin.setValue(0.01)
        self.settigns.agent_settings.gamma=0.95

    def reject_new_agent_settings(self):
        self.agent_creation_window.close()

    def set_current_values_in_details_windows(self):
        self.agent_details_ui.replay_size_spin.setValue(self.settigns.agent_settings.replay_size)
        self.agent_details_ui.mini_batch_size_zpin.setValue(self.settigns.agent_settings.mini_batch)
        self.agent_details_ui.exploration_decay_spin.setValue(self.settigns.agent_settings.exploration_decay)

        self.agent_details_ui.learning_rate_spin.setValue(self.settigns.agent_settings.learning_rate)
        self.agent_details_ui.mnimal_exploration_spin.setValue( self.settigns.agent_settings.mnimal_exploration)

    def accept_new_agent_details_settings(self):
        self.settigns.agent_settings.replay_size=self.agent_details_ui.replay_size_spin.value()
        self.settigns.agent_settings.mini_batch=self.agent_details_ui.mini_batch_size_zpin.value()
        self.settigns.agent_settings.exploration_decay=self.agent_details_ui.exploration_decay_spin.value()

        self.settigns.agent_settings.learning_rate=self.agent_details_ui.learning_rate_spin.value()
        self.settigns.agent_settings.mnimal_exploration=self.agent_details_ui.mnimal_exploration_spin.value()
        self.agent_details_window.close()

    def reject_new_agent_details_settings(self):
        self.agent_details_window.close()

    def set_default_agent_details(self):

        if not (self.agent_creation_window.isVisible()):
            if self.settigns.agent_settings.algorithm=="Deep Q-Learning":
                self.settigns.agent_settings.set_dqn_default()

                self.set_current_values_in_details_windows()

            if self.settigns.agent_settings.algorithm == "Strategia Gradientowa":
                self.settigns.agent_settings.set_pg_default()

                self.set_default_agent_pg_details()
            if self.agent_creation_ui.algorithm_slection.currentText() == "Advantage Actor Critic":
                self.set_default_agent_a2c_details()
                self.settigns.agent_settings.set_a2c_default()
            if  self.agent_creation_ui.algorithm_slection.currentText() == "Proximal Policy Optimization":
                self.set_default_agent_ppo_details()
                if settigns.game_settings.game_name=="cartpole":
                    self.settigns.agent_settings.set_ppo_cartpole_default()
                if settigns.game_settings.game_name=="Pong":
                    self.settigns.agent_settings.set_ppo_pong_default()


        else:

            if self.agent_creation_ui.algorithm_slection.currentText()=="Deep Q-Learning":
                self.settigns.agent_settings.algorithm = "Deep Q-Learning"
                self.settigns.agent_settings.set_dqn_default()
                self.set_current_values_in_agent_creation_form()
            if self.agent_creation_ui.algorithm_slection.currentText() == "Strategia Gradientowa":
                self.settigns.agent_settings.algorithm = "Strategia Gradientowa"
                self.settigns.agent_settings.set_pg_default()
                self.set_current_values_in_agent_creation_form()
            if self.agent_creation_ui.algorithm_slection.currentText() == "Advantage Actor Critic":
                self.settigns.agent_settings.set_a2c_cartpole_default()
                self.set_current_values_in_agent_creation_form()
            if self.agent_creation_ui.algorithm_slection.currentText() == "Proximal Policy Optimization":
                if settigns.game_settings.game_name == "cartpole":
                    self.settigns.agent_settings.set_ppo_cartpole_default()
                if settigns.game_settings.game_name == "Pong":
                    self.settigns.agent_settings.set_ppo_pong_default()
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
