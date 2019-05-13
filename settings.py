class AgentSettings():
    def __init__(self,algorithm):
        self.algorithm = algorithm
        self.gamma=0.1
        self.replay_size =2000
        self.mini_batch = 200
        self.exploration_decay =0.01
        self.start_exploration_value =0.99
        self.learning_rate = 0.1
        self.mnimal_exploration = 0.01


class GameSettings():
    def __init__(self,max_episodes=1000,accuracy=90,episodes_batch_size=10):
        self.max_episodes = max_episodes
        self.target_accuracy=accuracy
        self.episodes_batch_size=episodes_batch_size



class Settings():



    def __init__(self,algorithm="Deep Q-Learning"):
        self.agent_settings=AgentSettings(algorithm)
        self.game_settings=GameSettings()

