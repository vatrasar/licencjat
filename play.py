from settings import *
import gym
from AgentDQN import DQNAgent
import numpy as np
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from statistics import Statistics

class Play(QThread):


    signal_plot = pyqtSignal()
    def __init__(self, settigns:Settings):
        QThread.__init__(self)
        self.settigns=settigns
        self.statistics=Statistics(settigns.game_settings.episodes_batch_size,self.signal_plot)


    def __del__(self):
        self.wait()



    def run(self):

        # In case of CartPole-v1, maximum length of episode is 500
        env = gym.make('CartPole-v1')
        # get size of state and action from environment
        state_size = env.observation_space.shape[0]
        action_size = env.action_space.n

        agent = DQNAgent(state_size, action_size)



        for e in range(self.settigns.game_settings.max_episodes):
            done = False
            score = 0
            state = env.reset()
            state = np.reshape(state, [1, state_size])

            while not done:
                if agent.render:
                    env.render()

                # get action for the current state and go one step in environment
                action = agent.get_action(state)
                next_state, reward, done, info = env.step(action)
                next_state = np.reshape(next_state, [1, state_size])
                # if an action make the episode end, then gives penalty of -100
                reward = reward if not done or score == 499 else -100

                # save the sample <s, a, r, s'> to the replay memory
                agent.append_sample(state, action, reward, next_state, done)
                # every time step do the training
                agent.train_model()
                score += reward
                state = next_state

                if done:
                    # every episode update the target model to be same with model
                    agent.update_target_model()

                    # every episode, plot the play time
                    score = score if score == 500 else score + 100
                    self.statistics.append_score(score)





