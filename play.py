from settings import *
import gym
from agents.AgentDQN import DQNAgentBaseline
from agents.AgentDQN import DQNAgent
import numpy as np
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from statistics import Statistics
from keras import backend
from agents.agentPG import AgentPG
from agents.agentPG import AgentPGPong
from agents.agentA2C import A2CAgent
from agents.agentA2C import A2CAgentBaseline
from agents.agentPPO import AgentPPO
from statistics import StatisticsBaseline
from conf import game_type
from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.common.vec_env import VecFrameStack
import time
import tensorflow as tf
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines.common.vec_env import DummyVecEnv
import datetime
from conf import environments


class Play(QThread):


    signal_plot = pyqtSignal()
    signal_episode = pyqtSignal("int","double","double","int")
    signal_done=pyqtSignal("int","int")
    def __init__(self, settigns:Settings, render, is_tests,agent_to_load_directory,is_agent_to_load):
        QThread.__init__(self)
        self.settigns=settigns
        self.statistics=Statistics(settigns.curve_batch_size,self.signal_plot)
        self.render=render
        self.is_tests=is_tests
        # In case of CartPole-v1, maximum length of episode is 500
        self.env = gym.make('CartPole-v1')
        # get size of state and action from environment
        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n
        self.a = self.settigns.agent_settings
        self.agent_to_load_directory=agent_to_load_directory
        self.is_agent_to_load=is_agent_to_load
        self.settigns=settigns
        # if settigns.agent_settings.algorithm == "Advantage Actor Critic":
        #     if not(is_tests):
        #         n_cpu = 8
        #         self.env = SubprocVecEnv([lambda: gym.make('CartPole-v1') for i in range(n_cpu)])
        #     else:
        #         self.env = DummyVecEnv([lambda: self.env])
        #     statistics = StatisticsBaseline(self.settigns.curve_batch_size, self.signal_plot)
        #     self.agent = A2CAgentBaseline(self.state_size, self.action_size, self.settigns.agent_settings,is_agent_to_load, self.env, self.signal_done,
        #                           self.signal_episode, statistics, self.settigns.game_settings, game_type[settigns.game_settings.game_name],agent_to_load_directory, self.settigns.game_settings.game_name)


        if self.settigns.agent_settings.algorithm == "Strategia Gradientowa":
            self.agent = AgentPG(self.state_size, self.action_size,self.a, self.is_agent_to_load, self.agent_to_load_directory)


        if self.settigns.agent_settings.algorithm == "Proximal Policy Optimization":
            statistics = StatisticsBaseline(self.settigns.curve_batch_size, self.signal_plot)


            self.agent = AgentPPO(self.state_size, self.action_size, self.settigns.agent_settings, self.is_agent_to_load,
                                  self.env, self.signal_done,
                                  self.signal_episode, statistics, self.settigns.game_settings,
                                  game_type[self.settigns.game_settings.game_name], self.agent_to_load_directory,
                                  self.settigns.game_settings.game_name)
    def __del__(self):
        self.wait()



    def run(self):

        if self.settigns.agent_settings.algorithm == "Deep Q-Learning":
            # statistics = StatisticsBaseline(self.settigns.game_settings.episodes_batch_size, self.signal_plot)
            # self.agent = DQNAgent(self.state_size, self.action_size, self.settigns.agent_settings, is_agent_to_load,self.env,self.signal_done,self.signal_episode,statistics,self.settigns.game_settings,game_type[settigns.game_settings.game_name],agent_to_load_directory,self.settigns.game_settings.game_name)
            self.agent = DQNAgent(self.state_size, self.action_size, self.settigns.agent_settings, self.is_agent_to_load)

        if self.settigns.agent_settings.algorithm == "Advantage Actor Critic":
            self.agent = A2CAgent(self.state_size, self.action_size, self.settigns.agent_settings, self.is_agent_to_load,
                                  self.agent_to_load_directory,self.settigns.game_settings.game_name)




        done_signal_emited=False

        if not(self.agent.is_baseline) or self.is_tests==True:

            episodes=1
            steps=0

            while True:
                done = False
                score = 0
                state = self.env.reset()
                if not (self.agent.is_baseline):
                    #baseline is here during tests
                    state = np.reshape(state, [1, self.state_size])

                while not done:
                    if self.render:
                        self.env.render()

                    # get action for the current state and go one step in environment
                    action = self.agent.get_action(state)
                    next_state, reward, done, info = self.env.step(action)
                    steps+=1


                    if not(self.agent.is_baseline):#baseline is here during tests
                        next_state = np.reshape(next_state, [1, self.state_size])
                    # if an action make the episode end, then gives penalty of -100

                    reward = reward if not done or score == 499 else -100

                    # save the sample <s, a, r, s'> to the replay memory
                    self.agent.append_sample(state, action, reward, next_state, done)
                    # every time step do the training
                    if not (self.agent.is_baseline):#baseline is here during tests
                        self.agent.train_model()
                    score += reward
                    state = next_state

                    if done:
                        # every episode update the target model to be same with model
                        self.agent.update_target_model()

                        # every episode, plot the play time
                        score = score if score == 500 else score + 100
                        self.signal_episode.emit(episodes, self.statistics.get_current_mean_score(),score,steps)
                        self.statistics.append_score(score)
                if self.statistics.get_current_mean_score() >= self.settigns.game_settings.target_accuracy and not(self.is_tests):
                    self.signal_done.emit(
                        episodes+1, self.statistics.get_current_mean_score())
                    done_signal_emited=True

                    break
                episodes+=1
                if self.is_tests and episodes>self.settigns.game_settings.max_episodes_number:
                    self.signal_done.emit(episodes,
                                          self.statistics.get_current_mean_score())

                    break
                if not(self.is_tests) and steps>self.settigns.game_settings.max_steps_number:
                    self.signal_done.emit(episodes,
                                          self.statistics.get_current_mean_score())
                    done_signal_emited = True
                    break

        else:
            if  not(self.is_tests):
                self.agent.train_model()
                done_signal_emited=True


        if not(done_signal_emited):
            self.signal_done.emit(self.settigns.game_settings.max_episodes,self.statistics.get_current_mean_score())
        if not(self.is_tests):
            self.agent.save_model()
        backend.clear_session()
        tf.reset_default_graph()
        self.env.close()

class PlayAtari(QThread):


    signal_plot = pyqtSignal()
    signal_episode = pyqtSignal("int","double","double","int")
    signal_done=pyqtSignal("int","int")
    def __init__(self, settigns:Settings, render, is_tests,agent_to_load_directory,is_agent_to_load):
        QThread.__init__(self)
        self.settigns=settigns
        self.statistics=Statistics(self.settigns.curve_batch_size,self.signal_plot)
        self.render=render
        self.is_tests=is_tests
        # In case of CartPole-v1, maximum length of episode is 500
        if "Strategia Gradientowa"==self.settigns.agent_settings.algorithm:
            self.env = gym.make("Pong-v0")


        else:

            self.env = make_atari_env(environments[settigns.game_settings.game_name], num_env=1, seed=0)
            self.env = VecFrameStack(self.env, n_stack=4)


        # get size of state and action from environment
        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n
        a = self.settigns.agent_settings


        if self.settigns.agent_settings.algorithm == "Deep Q-Learning":
            statistics = StatisticsBaseline(self.settigns.curve_batch_size, self.signal_plot)
            self.agent = DQNAgentBaseline(self.state_size, self.action_size, self.settigns.agent_settings, is_agent_to_load,self.env,self.signal_done,self.signal_episode,statistics,self.settigns.game_settings,game_type[settigns.game_settings.game_name],agent_to_load_directory,self.settigns.game_settings.game_name)

        if self.settigns.agent_settings.algorithm == "Strategia Gradientowa":
            self.agent = AgentPGPong(self.state_size, self.action_size, a, is_agent_to_load,agent_to_load_directory)

        if self.settigns.agent_settings.algorithm == "Advantage Actor Critic":
            statistics = StatisticsBaseline(self.settigns.curve_batch_size, self.signal_plot)
            self.agent = A2CAgentBaseline(self.state_size, self.action_size, self.settigns.agent_settings,is_agent_to_load, self.env, self.signal_done,
                                  self.signal_episode, statistics, self.settigns.game_settings, game_type[settigns.game_settings.game_name],agent_to_load_directory, self.settigns.game_settings.game_name)

        if self.settigns.agent_settings.algorithm == "Proximal Policy Optimization":
            statistics = StatisticsBaseline(self.settigns.curve_batch_size, self.signal_plot)
            self.agent = AgentPPO(self.state_size, self.action_size, self.settigns.agent_settings,is_agent_to_load, self.env, self.signal_done,
                                  self.signal_episode, statistics, self.settigns.game_settings, game_type[settigns.game_settings.game_name],agent_to_load_directory, self.settigns.game_settings.game_name)



    def __del__(self):
        self.wait()



    def run(self):


        self.agent.start_time=time.time()

        episodes = 0
        steps = 0
        done_signal_emited=False

        if not(self.agent.is_baseline) or self.is_tests==True:

            while True:
                done = False
                score = 0
                state = self.env.reset()


                while not done:
                    if self.render:
                        self.env.render()
                        time.sleep(0.04)


                    # get action for the current state and go one step in environment
                    action = self.agent.get_action(state)
                    next_state, reward, done, info = self.env.step(action)
                    # if not(self.agent.is_baseline):#baseline is here during tests
                    #     next_state = np.reshape(next_state, [1, self.state_size])
                    # if an action make the episode end, then gives penalty of -100

                    # reward = reward if not done or score == 499 else -100

                    # save the sample <s, a, r, s'> to the replay memory
                    self.agent.append_sample(state, action, reward, next_state, done)
                    # every time step do the training

                    score += reward
                    state = next_state
                    steps += 1
                    if done:
                        # every episode update the target model to be same with model
                        if not(self.agent.is_baseline):
                            self.agent.train_model()
                        self.signal_episode.emit(episodes, self.statistics.get_current_mean_score(), score, steps)

                        # every episode, plot the play time
                        # score = score if score == 500 else score + 100
                        self.statistics.append_score(score)
                if self.statistics.get_current_mean_score() >= self.settigns.game_settings.target_accuracy and not (
                self.is_tests):
                    self.signal_done.emit(
                        episodes, self.statistics.get_current_mean_score())
                    done_signal_emited = True

                    break
                episodes += 1
                if self.is_tests and episodes >= self.settigns.game_settings.max_episodes_number:
                    self.signal_done.emit(episodes,
                                          self.statistics.get_current_mean_score())
                    done_signal_emited = True

                    break
                if not (self.is_tests) and steps > self.settigns.game_settings.max_steps_number:
                    self.signal_done.emit(episodes,
                                          self.statistics.get_current_mean_score())
                    done_signal_emited = True
                    break
        else:
            if  self.is_tests!=True:
                self.agent.train_model()
                done_signal_emited=True

        if not (done_signal_emited):
            self.signal_done.emit(self.settigns.game_settings.max_episodes, self.statistics.get_current_mean_score())
        if not (self.is_tests):
            self.agent.save_model()
        backend.clear_session()
        tf.reset_default_graph()
        if self.render:
            self.env.venv.envs[0].unwrapped.viewer.window.close()









