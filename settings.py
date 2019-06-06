import conf

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
        # self.gamma = 0.99
        # self.replay_size = 50000
        # self.mini_batch = 32
        # self.exploration_decay = 0.1
        # self.start_exploration_value = 1
        # self.learning_rate = 0.0005
        # self.mnimal_exploration = 0.02
    def set_dqn_atari_default(self):

        self.gamma = 0.99
        self.replay_size = 10000
        self.mini_batch = 256
        self.exploration_decay = 0.1
        self.start_exploration_value = 1
        self.learning_rate = 1e-4
        self.mnimal_exploration = 0.01
        # self.gamma = 0.99
        # self.replay_size = 50000
        # self.mini_batch = 32
        # self.exploration_decay = 0.1
        # self.start_exploration_value = 1
        # self.learning_rate = 0.0005
        # self.mnimal_exploration = 0.02

    def set_pg_default(self):
        self.gamma=0.95
        self.learning_rate=0.01

    def set_pg_pong_default(self):
        self.gamma=0.99
        self.learning_rate=0.0006

    def set_a2c_cartpole_default(self):
        self.algorithm="Advantage Actor Critic"
        self.gamma=0.99
        self.critic_lr=0.001
        self.actor_lr=0.005
        self.gamma=0.99
        # self.critic_lr=0.25
        # self.actor_lr=0.0007
        self.c2 = 0.00

    def set_a2c_atari_default(self):
        self.algorithm = "Advantage Actor Critic"
        self.gamma = 0.99
        self.critic_lr = 0.25
        self.actor_lr = 0.0007
        self.c2=0.01

    def set_ppo_cartpole_default(self):
        self.algorithm = "Proximal Policy Optimization"
        self.c1 = 0.95
        self.c2 = 0.01
        self.clip_epslion = 0.2
        self.gamma=0.98

    def set_ppo_atari_default(self):
        self.algorithm = "Proximal Policy Optimization"
        self.c1 = 0.95
        self.c2 = 0.01
        self.clip_epslion = 0.2
        self.gamma=0.99


class GameSettings():
    def __init__(self,max_steps_number=25000,accuracy=90,episodes_batch_size=10,max_episodes_number=3):
        self.max_steps_number = max_steps_number
        self.max_episodes_number = max_episodes_number
        self.target_accuracy=accuracy
        self.episodes_batch_size=episodes_batch_size
        self.game_name="Pong"




class Settings():



    def __init__(self,algorithm="Deep Q-Learning"):
        self.agent_settings=AgentSettings(algorithm)
        self.game_settings=GameSettings()
        self.conf_defaults={
            "atari": {
                "Deep Q-Learning": self.agent_settings.set_dqn_atari_default,
                "Proximal Policy Optimization":self.agent_settings.set_ppo_atari_default,
                "Advantage Actor Critic":self.agent_settings.set_a2c_atari_default,
                "Strategia Gradientowa":self.agent_settings.set_pg_pong_default
            },
            "box": {
                "Deep Q-Learning": self.agent_settings.set_dqn_default,
                "Proximal Policy Optimization": self.agent_settings.set_ppo_cartpole_default,
                "Advantage Actor Critic": self.agent_settings.set_a2c_cartpole_default,
                "Strategia Gradientowa": self.agent_settings.set_pg_default
            }
        }

    def set_default_for_algorithm(self,algorithm):
        self.agent_settings.algorithm=algorithm
        self.conf_defaults[conf.game_type[self.game_settings.game_name]][algorithm]()






