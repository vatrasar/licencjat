

class BaseAgent():
    def __init__(self, state_size, action_size, agent_settings, is_agent_to_load,game_name):
        self.gamma = agent_settings.gamma  # Discount rate
        self.state_size = state_size
        self.action_size = action_size
        self.is_baseline=False
        self.game_name=game_name


    def build_model(self):
        pass

    def update_target_model(self):
        pass

    def get_action(self,state):
        pass

    def append_sample(self,state, action, reward, next_state, done):
        pass

    def save_model(self):
        pass

    def load_model(self,agent_to_load_directory):
        pass

    def train_model(self):
        pass