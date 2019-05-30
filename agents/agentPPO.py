from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.policies import MlpLstmPolicy
from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.common.policies import CnnPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO1
from agents.baseAgent import BaseAgent
from statistics import StatisticsBaseline
import time
import datetime

class AgentPPO(BaseAgent):
    def __init__(self, state_size, action_size, agent_settings, is_agent_to_load, env, signal_done, signal_episode,
                 statistic: StatisticsBaseline,game_settings,game_type,agent_to_load_directory,game_name):
        """

        :param state_size:
        :param action_size:
        :param agent_settings:
        :param is_agent_to_load:
        :param env:
        :param signal_done:
        :param signal_episode:
        :param statistic:
        :param game_settings:
        :param game_type: can be box or atari
        """
        super().__init__(state_size, action_size, agent_settings, is_agent_to_load,game_name)
        self.env=env

        self.is_baseline=True
        self.signal_done=signal_done
        self.signal_episde=signal_episode

        self.statistic=statistic
        self.game_settings=game_settings
        self.c1=agent_settings.c1
        self.c2=agent_settings.c2
        self.clip_epslion=agent_settings.clip_epslion
        self.game_type=game_type
        self.start_time=time.time()
        self.last_save_time=time.time()
        if is_agent_to_load:
            self.load_model(agent_to_load_directory)
        else:
            self.build_model()
            

    def build_model(self):

        if self.game_type=="box":
            self.env = DummyVecEnv([lambda: self.env])
            self.model = PPO1(MlpPolicy, self.env, verbose=0,gamma=self.gamma,lam=self.c1,entcoeff=self.c2,clip_param=self.clip_epslion)
        if self.game_type=="atari":

            self.model = PPO1(CnnPolicy, self.env, verbose=1,gamma=self.gamma,lam=self.c1,entcoeff=self.c2,clip_param=self.clip_epslion)

    def update_target_model(self):
        super().update_target_model()

    def get_action(self, state):
        action, _states = self.model.predict(state)
        return action

    def append_sample(self, state, action, reward, next_state, done):
        super().append_sample(state, action, reward, next_state, done)

    def save_model(self,file_name="./models/agentPPO"):
        self.model.save(file_name)
        out=open(file_name+".txt","w")
        out.write(self.game_name)
        out.close()

    def load_model(self,agent_to_load_directory):
        if  agent_to_load_directory=="":
            self.model=PPO1.load("./models/agentPPO.pkl",env=self.env)
        else:
            self.model=PPO1.load(agent_to_load_directory,env=self.env)

    def train_model(self):

        self.model.learn(total_timesteps=self.game_settings.max_steps_number,callback=self.callback)


    def callback(self,_locals, _globals):
        self.statistic.append_score(_locals['rewbuffer'],_locals['episodes_so_far'])

        self.signal_episde.emit(_locals['episodes_so_far'])

        if self.statistic.get_current_mean_score()>=self.game_settings.target_accuracy or _locals['episodes_so_far']>self.game_settings.max_steps_number:
            self.signal_done.emit(_locals['episodes_so_far'], self.statistic.get_current_mean_score())
            self.done=True
            output=open("./models/trenningResults.txt","w")
            output.write("czas trening:"+str((time.time()-self.start_time)/3600)+"h \n")
            output.write("liczba epizodów:"+str(_locals['episodes_so_far']) + "\n")
            output.write("liczba kroków:" + str(_locals['timesteps_so_far']) + "\n")
            output.close()

            return False
        if time.time()-self.last_save_time>60*10:


            self.last_save_time=time.time()

            self.save_model("./models/agentPPOtemp")
        return True




