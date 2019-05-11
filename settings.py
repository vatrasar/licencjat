class AgentSettings():
    def __init__(self,algorithm):
        self.algorithm = algorithm


class Settings():



    def __init__(self,algorithm="Deep Q-Learning"):
        self.agent_settings=AgentSettings(algorithm)

