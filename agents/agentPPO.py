from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO1
from agents.baseAgent import BaseAgent
from statistics import StatisticsBaseline




class AgentPPO(BaseAgent):
    def __init__(self, state_size, action_size, agent_settings, is_agent_to_load, env, signal_done, signal_episode,
                 statistic: StatisticsBaseline,game_settings):
        super().__init__(state_size, action_size, agent_settings, is_agent_to_load)
        self.env=env
        self.build_model()
        self.is_baseline=True
        self.signal_done=signal_done
        self.signal_episde=signal_episode
        self.statistic=statistic
        self.game_settings=game_settings

    def build_model(self):
        self.env = DummyVecEnv([lambda: self.env])
        self.model = PPO1(MlpPolicy, self.env, verbose=1)

    def update_target_model(self):
        super().update_target_model()

    def get_action(self, state):
        action, _states = self.model.predict(state)
        return action

    def append_sample(self, state, action, reward, next_state, done):
        super().append_sample(state, action, reward, next_state, done)

    def save_model(self):
        self.model.save("./models/agentPPO")

    def load_model(self):
        self.model=PPO1.load("./models/agentPPO")

    def train_model(self):
        self.model.learn(total_timesteps=25000,log_interval=50)


    def callback(self,_locals, _globals):
        self.statistic.append_score(_locals['rewbuffer'],_locals['episodes_so_far'])

        self.signal_episde.emit(_locals['episodes_so_far'])
        if self.statistic.get_current_mean_score()>=self.game_settings.self.target_accuracy or _locals['episodes_so_far']>self.game_settings.max_episodes:
            self.signal_done.emit(_locals['episodes_so_far'], self.statistic.get_current_mean_score())
            return False
        return True


