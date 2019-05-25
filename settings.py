class AgentSettings():
    def __init__(self,algorithm):
        self.algorithm = algorithm
        self.gamma=0.99
        self.replay_size =2000
        self.mini_batch = 64
        self.exploration_decay =0.999
        self.start_exploration_value =1
        self.learning_rate = 0.001
        self.mnimal_exploration = 0.01
        self.actor_lr = 0.001
        self.critic_lr = 0.005
        self.c1=0
        self.c2=0
        self.clip_epslion=0.1

    def set_dqn_default(self):

        self.gamma = 0.99
        self.replay_size = 2000
        self.mini_batch = 64
        self.exploration_decay = 0.999
        self.start_exploration_value = 1
        self.learning_rate = 0.001
        self.mnimal_exploration = 0.01

    def set_pg_default(self):
        self.gamma=0.95
        self.learning_rate=0.01

    def set_a2c_cartpole_default(self):
        self.algorithm="Advantage Actor Critic"
        self.gamma=0.99
        self.critic_lr=0.001
        self.actor_lr=0.005
    def set_ppo_default(self):
        self.algorithm = "Proximal Policy Optimization"
        self.c1 = 0.95
        self.c2 = 0.01
        self.clip_epslion = 0.2
        self.gamma=0.99


class GameSettings():
    def __init__(self,max_episodes=1000,accuracy=90,episodes_batch_size=10):
        self.max_episodes = max_episodes
        self.target_accuracy=accuracy
        self.episodes_batch_size=episodes_batch_size
        self.game_name="Pong"




class Settings():



    def __init__(self,algorithm="Deep Q-Learning"):
        self.agent_settings=AgentSettings(algorithm)
        self.game_settings=GameSettings()




