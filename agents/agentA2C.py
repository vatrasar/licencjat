from agents.baseAgent import BaseAgent
import gym


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














