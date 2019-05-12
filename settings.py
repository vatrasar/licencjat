class AgentSettings():
    def __init__(self,algorithm):
        self.algorithm = algorithm


class GameSettings():
    def __init__(self,max_episodes=1000,accuracy=90):
        self.max_episodes = max_episodes
        self.target_accuracy=accuracy


class Settings():



    def __init__(self,algorithm="Deep Q-Learning"):
        self.agent_settings=AgentSettings(algorithm)
        self.game_settings=GameSettings()

