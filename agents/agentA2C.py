from agents.baseAgent import BaseAgent
import gym
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.policies import MlpLstmPolicy
from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.common.policies import CnnPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C
from agents.baseAgent import BaseAgent
from statistics import StatisticsBaseline

from stable_baselines.common.policies import CnnLstmPolicy
import time
import datetime

import numpy as np

#
# class AgentA2C(BaseAgent):
#     def __init__(self, state_size, action_size, agent_settings, is_agent_to_load,env,max_episodes):
#         super().__init__(state_size, action_size, agent_settings, is_agent_to_load)
#         self.env=env
#         self.env = Monitor(env, "./monitor", allow_early_resets=True)
#         self.max_episodes=max_episodes
#         self.current_episode=0
#         self.is_baseline=True
#         self.env = DummyVecEnv([lambda: self.env])
#         self.build_model()
#
#     def build_model(self):
#         self.model = A2C(MlpPolicy, self.env, verbose=1,gamma=0.99,learning_rate=0.001)
#
#     def get_action(self, state):
#         action, _states = self.model.predict(state)
#         return action
#
#     def train_model(self):
#         self.current_episode = 0
#         self.model.learn(total_timesteps=500*self.max_episodes,callback=self.callback)
#
#     def callback(self,_locals, _globals):
#         """
#         Callback called at each step (for DQN an others) or after n steps (see ACER or PPO2)
#         :param _locals: (dict)
#         :param _globals: (dict)
#         """
#         global n_steps, best_mean_reward
#
#         x, y = ts2xy(load_results("./monitor"), 'episodes')
#         if x.__len__()>100:
#             print(y[-100:].mean())
#         return True




import sys
import gym
import pylab
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam




# A2C(Advantage Actor-Critic) agent for the Cartpole
class A2CAgent(BaseAgent):
    def __init__(self, state_size, action_size, agent_settings, is_agent_to_load,agent_to_load_directory,game_name):
        super().__init__(state_size, action_size, agent_settings, is_agent_to_load,game_name)
        self.actor_lr = agent_settings.actor_lr
        self.critic_lr = agent_settings.critic_lr
        self.value_size = 1
        self.build_model()

        if is_agent_to_load:
            self.load_model(agent_to_load_directory)

    def build_model(self):
        self.build_actor()
        self.build_critic()

    def load_model(self,agent_to_load_directory):
        self.actor.load_weights("./models/cartpole_actor.h5")
        self.critic.load_weights("./models/cartpole_critic.h5")


    def build_actor(self):
        self.actor = Sequential()
        self.actor.add(Dense(24, input_dim=self.state_size, activation='relu',
                        kernel_initializer='he_uniform'))
        self.actor.add(Dense(self.action_size, activation='softmax',
                        kernel_initializer='he_uniform'))
        self.actor.summary()
        # See note regarding crossentropy in cartpole_reinforce.py
        self.actor.compile(loss='categorical_crossentropy',
                      optimizer=Adam(lr=self.actor_lr))


    # critic: state is input and value of state is output of model
    def build_critic(self):
        self.critic = Sequential()
        self.critic.add(Dense(24, input_dim=self.state_size, activation='relu',
                         kernel_initializer='he_uniform'))
        self.critic.add(Dense(self.value_size, activation='linear',
                         kernel_initializer='he_uniform'))
        self.critic.summary()
        self.critic.compile(loss="mse", optimizer=Adam(lr=self.critic_lr))



    def get_action(self, state):
        policy = self.actor.predict(state, batch_size=1).flatten()
        return np.random.choice(self.action_size, 1, p=policy)[0]

    def append_sample(self, state, action, reward, next_state, done):
        target = np.zeros((1, self.value_size))
        advantages = np.zeros((1, self.action_size))

        value = self.critic.predict(state)[0]
        next_value = self.critic.predict(next_state)[0]

        if done:
            advantages[0][action] = reward - value
            target[0][0] = reward
        else:
            advantages[0][action] = reward + self.gamma * (next_value) - value
            target[0][0] = reward + self.gamma* next_value

        self.actor.fit(state, advantages, epochs=1, verbose=0)
        self.critic.fit(state, target, epochs=1, verbose=0)

    def save_model(self):
        self.actor.save_weights("./models/cartpole_actor.h5")
        self.critic.save_weights("./models/cartpole_critic.h5")

    # update policy network every episode


class A2CAgentBaseline(BaseAgent):
    def __init__(self, state_size, action_size, agent_settings, is_agent_to_load, env, signal_done, signal_episode,
                 statistic: StatisticsBaseline,game_settings,game_type,agent_to_load_directory,game_name,is_multienv):
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
        super().__init__(state_size, action_size, agent_settings, is_agent_to_load, game_name)
        self.env = env

        self.is_baseline = True
        self.signal_done = signal_done
        self.signal_episde = signal_episode

        self.statistic = statistic
        self.game_settings = game_settings
        self.c1 =  agent_settings.critic_lr
        self.c2 = agent_settings.c2
        self.actor_lr=agent_settings.actor_lr
        self.critic_lr=agent_settings.critic_lr
        self.episodes=0
        self.game_type = game_type
        self.start_time = time.time()
        self.last_save_time = time.time()
        self.episodes_number=0
        self.is_multienv=True
        if is_agent_to_load:
            self.load_model(agent_to_load_directory)
        else:
            self.build_model()
        if self.game_type == "atari":
            self.is_multienv = is_multienv

    def build_model(self):

        if self.game_type == "box":
            self.env = DummyVecEnv([lambda: self.env])
            self.model = A2C(MlpPolicy, self.env, verbose=0, gamma=self.gamma, learning_rate =self.actor_lr, ent_coef=self.c2,vf_coef=self.critic_lr)
        if self.game_type == "atari":
            self.model = A2C(CnnLstmPolicy, self.env, verbose=0, gamma=self.gamma, learning_rate =self.actor_lr, ent_coef=self.c2,vf_coef=self.critic_lr)

    def update_target_model(self):
        super().update_target_model()

    def get_action(self, state):
        action, _states = self.model.predict(state)
        return action

    def append_sample(self, state, action, reward, next_state, done):
        super().append_sample(state, action, reward, next_state, done)

    def save_model(self, file_name="./models/agentA2c"):
        self.model.save(file_name)
        out = open(file_name + ".txt", "w")
        out.write(self.game_name)
        out.close()

    def load_model(self, agent_to_load_directory,is_test=False):
        if self.game_type != "atari":
            if agent_to_load_directory == "":
                self.model = A2C.load("./models/agentPPO.pkl", env=self.env)
            else:
                self.model = A2C.load(agent_to_load_directory, env=self.env)
        else:
            if is_test:
                if agent_to_load_directory == "":
                    self.model = A2C.load("./models/agentPPO.pkl")
                else:
                    self.model = A2C.load(agent_to_load_directory)
            else:
                if agent_to_load_directory == "":
                    self.model = A2C.load("./models/agentPPO.pkl", env=self.env)
                else:
                    self.model = A2C.load(agent_to_load_directory, env=self.env)

    def train_model(self):

        self.model.learn(total_timesteps=self.game_settings.max_steps_number, callback=self.callback)

    def callback(self, _locals, _globals):
        # steps=_locals['update']*5
        # if _locals['ep_infos'].__len__()>=1:
        #     self.episodes+=1
        #     self.statistic.append_a2c(_locals['ep_infos'][0]['r'], self.episodes)
        #     self.signal_episde.emit(self.episodes,self.statistic.get_current_mean_score(),_locals['ep_infos'][0]['r'],steps)
        #
        #
        #
        # #
        # if self.statistic.get_current_mean_score() >= self.game_settings.target_accuracy or steps>=self.game_settings.max_steps_number:
        #     self.signal_done.emit(self.episodes, self.statistic.get_current_mean_score())
        #     self.done = True
        #     output = open("./models/trenningResults.txt", "w")
        #     output.write("czas trening:" + str((time.time() - self.start_time) / 3600) + "h \n")
        #     output.write("liczba epizodów:" + str(self.episodes) + "\n")
        #     output.write("liczba kroków:" + str(steps) + "\n")
        #     output.close()
        #
        #     # return False
        # if time.time() - self.last_save_time > 60 * 10:
        #     self.last_save_time = time.time()
        #
        #     self.save_model("./models/agentA2ctemp")
        # return True

        time_steps = _locals['update'] * _locals['runner'].n_steps * _locals['runner'].env.num_envs
        for epo in _locals['ep_infos']:
            self.episodes_number+=1
            self.statistic.append_a2c(epo['r'],self.episodes_number)
            self.signal_episde.emit(self.episodes_number,self.statistic.get_current_mean_score(),_locals['ep_infos'][-1]['r'],time_steps)

        if self.statistic.get_current_mean_score()>=self.game_settings.target_accuracy or time_steps>=self.game_settings.max_steps_number:
            self.signal_done.emit(self.episodes_number, self.statistic.get_current_mean_score())
            self.done=True
            output=open("./models/trenningResults.txt","w")
            output.write("czas trening:"+str((time.time()-self.start_time)/3600)+"h \n")
            output.write("liczba epizodów:"+str(self.episodes_number) + "\n")
            output.write("liczba kroków:" + str(time_steps) + "\n")
            output.close()

            return False
        if time.time()-self.last_save_time>60*10:

            self.last_save_time=time.time()

            self.save_model("./models/agentPPOtemp")
            output = open("./models/trenningResults.txt", "w")
            output.write("czas trening:" + str((time.time() - self.start_time) / 3600) + "h \n")
            output.write("liczba epizodów:" + str(self.episodes_number) + "\n")
            output.write("liczba kroków:" + str(time_steps) + "\n")
            output.close()
        return True














