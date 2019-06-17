import random
import numpy as np
from collections import deque
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential
from settings import AgentSettings
from agents.baseAgent import BaseAgent
from statistics import StatisticsBaseline
import time

from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.policies import MlpLstmPolicy
from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.deepq.policies import CnnPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN


class DQNAgent:
    def __init__(self, state_size, action_size, agent_settings,is_agent_to_load):
        # if you want to see Cartpole learning, then change to True
        self.render = False
        self.load_model = False
        self.is_baseline=False
        # get size of state and action
        self.state_size = state_size
        self.action_size = action_size

        self.is_agent_to_load=is_agent_to_load
        # These are hyper parameters for the DQN
        self.discount_factor = agent_settings.gamma
        self.learning_rate =agent_settings.learning_rate
        self.epsilon = 0.99
        self.epsilon_decay =1-agent_settings.exploration_decay
        self.epsilon_min = agent_settings.mnimal_exploration
        self.batch_size = agent_settings.mini_batch
        self.train_start = 1000

        # create replay memory using deque
        self.memory = deque(maxlen=agent_settings.replay_size)

        # create main model and target model
        self.model = self.build_model()
        self.target_model = self.build_model()

        # initialize target model
        self.update_target_model()
        if self.is_agent_to_load:
           self.model.load_weights("./models/agent.h5")




    # approximate Q function using Neural Network
    # state is input and Q Value of each action is output of network
    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu',
                        kernel_initializer='he_uniform'))
        model.add(Dense(24, activation='relu',
                        kernel_initializer='he_uniform'))
        model.add(Dense(self.action_size, activation='linear',
                        kernel_initializer='he_uniform'))
        model.summary()

        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

        return model

    # after some time interval update the target model to be same with model
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    # get action from model using epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            q_value = self.model.predict(state)
            return np.argmax(q_value[0])


    # save sample <s,a,r,s'> to the replay memory
    def append_sample(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay



    # pick samples randomly from replay memory (with batch_size)
    def train_model(self):
        if len(self.memory) < self.train_start:
            return
        batch_size = min(self.batch_size, len(self.memory))
        mini_batch = random.sample(self.memory, batch_size)

        update_input = np.zeros((batch_size, self.state_size))
        update_target = np.zeros((batch_size, self.state_size))
        action, reward, done = [], [], []

        for i in range(self.batch_size):
            update_input[i] = mini_batch[i][0]
            action.append(mini_batch[i][1])
            reward.append(mini_batch[i][2])
            update_target[i] = mini_batch[i][3]
            done.append(mini_batch[i][4])

        target = self.model.predict(update_input)
        target_val = self.target_model.predict(update_target)

        for i in range(self.batch_size):
            # Q Learning: get maximum Q value at s' from target model
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                target[i][action[i]] = reward[i] + self.discount_factor * (
                    np.amax(target_val[i]))

        # and do the model fit!
        self.model.fit(update_input, target, batch_size=self.batch_size,
                       epochs=1, verbose=0)

    def save_model(self):
        self.model.save_weights("./models/agent.h5")


class DQNAgentBaseline(BaseAgent):
    def __init__(self, state_size, action_size, agent_settings, is_agent_to_load, env, signal_done, signal_episode,
                 statistic: StatisticsBaseline, game_settings, game_type, agent_to_load_directory, game_name):
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



        self.gamma = agent_settings.gamma
        self.learning_rate = agent_settings.learning_rate
        self.epsilon_decay = agent_settings.exploration_decay
        self.epsilon_min = agent_settings.mnimal_exploration
        self.batch_size = agent_settings.mini_batch
        self.replay_size=agent_settings.replay_size


        self.last_episode_emited=0
        self.game_type = game_type
        self.start_time = time.time()
        self.last_save_time = time.time()
        if is_agent_to_load:
            self.load_model(agent_to_load_directory)
        else:
            self.build_model()
    def build_model(self):

        if self.game_type=="box":
            self.env = DummyVecEnv([lambda: self.env])
            self.model = DQN(MlpPolicy, self.env, verbose=0,gamma=self.gamma,exploration_fraction=self.epsilon_decay,exploration_final_eps=self.epsilon_min,learning_rate=self.learning_rate,buffer_size=self.replay_size,batch_size=self.batch_size)
        if self.game_type=="atari":

            self.model = DQN(CnnPolicy, self.env, verbose=1,gamma=self.gamma,exploration_fraction=self.epsilon_decay,exploration_final_eps=self.epsilon_min,learning_rate=self.learning_rate,buffer_size=self.replay_size,batch_size=self.batch_size)

    def update_target_model(self):
        super().update_target_model()

    def get_action(self, state):
        action, _states = self.model.predict(state)
        return action

    def append_sample(self, state, action, reward, next_state, done):
        super().append_sample(state, action, reward, next_state, done)

    def save_model(self,file_name="./models/agentDQN"):
        self.model.save(file_name)
        out=open(file_name+".txt","w")
        out.write(self.game_name)
        out.close()

    def load_model(self,agent_to_load_directory):
        if  agent_to_load_directory=="":
            self.model=DQN.load("./models/agentDQN.pkl",env=self.env)
        else:
            self.model=DQN.load(agent_to_load_directory,env=self.env)

    def train_model(self):

        self.model.learn(total_timesteps=self.game_settings.max_steps_number,callback=self.callback)


    def callback(self,_locals, _globals):
        self.statistic.append_score(_locals['episode_rewards'],_locals['episode_rewards'].__len__())

        if _locals['episode_rewards'].__len__()!=self.last_episode_emited and _locals['episode_rewards'].__len__()>1:
            self.signal_episde.emit(_locals['episode_rewards'].__len__()-1,self.statistic.get_current_mean_score(),_locals['episode_rewards'][-2],_locals['_'])
            self.last_episode_emited=_locals['episode_rewards'].__len__()

        if self.statistic.get_current_mean_score()>=self.game_settings.target_accuracy or _locals['_']+1>=self.game_settings.max_steps_number:
            self.signal_done.emit(_locals['episode_rewards'].__len__(), self.statistic.get_current_mean_score())
            self.done=True
            output=open("./models/trenningResults.txt","w")
            output.write("czas trening:"+str((time.time()-self.start_time)/3600)+"h \n")
            output.write("liczba epizodów:"+str(_locals['episode_rewards'].__len__()) + "\n")
            output.write("liczba kroków:" + str(_locals['_']) + "\n")
            output.close()

            return False
        if time.time()-self.last_save_time>60*10:
            output = open("./models/trenningResults.txt", "w")
            output.write("czas trening:" + str((time.time() - self.start_time) / 3600) + "h \n")
            output.write("liczba epizodów:" + str( _locals['episode_rewards'].__len__()) + "\n")
            output.write("liczba kroków:" + str(_locals['_']) + "\n")
            output.close()

            self.last_save_time=time.time()

            self.save_model("./models/agentDQNtemp")
        return True
