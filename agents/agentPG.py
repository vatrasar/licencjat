import tensorflow as tf
import numpy as np
import gym
from settings import Settings
from agents.baseAgent import BaseAgent


class AgentPG():


    def __init__(self,state_size, action_size,settings,is_agent_to_load,agent_to_load_directory):
        ## ENVIRONMENT Hyperparameters
        self.state_size = state_size
        self.action_size = action_size

        ## TRAINING Hyperparameters
        # max_episodes = 3000
        self.learning_rate = settings.learning_rate
        self.gamma = settings.gamma  # Discount rate
        self.episode_states, self.episode_actions, self.episode_rewards = [], [], []
        self.is_baseline=False
        self.build_model()
        if is_agent_to_load:
            self.load_model(agent_to_load_directory)


    def discount_and_normalize_rewards(self,episode_rewards):
        discounted_episode_rewards = np.zeros_like(episode_rewards)
        cumulative = 0.0
        for i in reversed(range(len(episode_rewards))):
            cumulative = cumulative * self.gamma + episode_rewards[i]
            discounted_episode_rewards[i] = cumulative

        mean = np.mean(discounted_episode_rewards)
        std = np.std(discounted_episode_rewards)
        discounted_episode_rewards = (discounted_episode_rewards - mean) / (std)

        return discounted_episode_rewards

    def build_model(self):
        tf.reset_default_graph()
        with tf.name_scope("inputs"):
            self.input_ = tf.placeholder(tf.float32, [None, self.state_size], name="input_")
            self.actions = tf.placeholder(tf.int32, [None, self.action_size], name="actions")
            self.discounted_episode_rewards_ = tf.placeholder(tf.float32, [None, ], name="discounted_episode_rewards")

            # Add this placeholder for having this variable in tensorboard
            self.mean_reward_ = tf.placeholder(tf.float32, name="mean_reward")

            with tf.name_scope("fc1"):
                self.fc1 = tf.contrib.layers.fully_connected(inputs=self.input_,
                                                        num_outputs=10,
                                                        activation_fn=tf.nn.relu,
                                                        weights_initializer=tf.contrib.layers.xavier_initializer())

            with tf.name_scope("fc2"):
                self.fc2 = tf.contrib.layers.fully_connected(inputs=self.fc1,
                                                        num_outputs=self.action_size,
                                                        activation_fn=tf.nn.relu,
                                                        weights_initializer=tf.contrib.layers.xavier_initializer())

            with tf.name_scope("fc3"):
                self.fc3 = tf.contrib.layers.fully_connected(inputs=self.fc2,
                                                        num_outputs=self.action_size,
                                                        activation_fn=None,
                                                        weights_initializer=tf.contrib.layers.xavier_initializer())

            with tf.name_scope("softmax"):
                self.action_distribution = tf.nn.softmax(self.fc3)

            with tf.name_scope("loss"):
                # tf.nn.softmax_cross_entropy_with_logits computes the cross entropy of the result after applying the softmax function
                # If you have single-class labels, where an object can only belong to one class, you might now consider using
                # tf.nn.sparse_softmax_cross_entropy_with_logits so that you don't have to convert your labels to a dense one-hot array.
                self.neg_log_prob = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.fc3, labels=self.actions)
                self.loss = tf.reduce_mean(self.neg_log_prob * self.discounted_episode_rewards_)

            with tf.name_scope("train"):
                self.train_opt = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)



            self.sess=tf.Session()
            self.sess.run(tf.global_variables_initializer())
            self.saver =tf.train.Saver()


    def get_action(self,state):
        action_probability_distribution = self.sess.run(self.action_distribution, feed_dict={self.input_: state.reshape([1, 4])})

        return np.random.choice(range(action_probability_distribution.shape[1]),
                                  p=action_probability_distribution.ravel())

    def update_target_model(self):
        # Calculate discounted reward
        discounted_episode_rewards = self.discount_and_normalize_rewards(self.episode_rewards)


        # Feedforward, gradient and backpropagation
        loss_, _ = self.sess.run([self.loss, self.train_opt], feed_dict={self.input_: np.vstack(np.array(self.episode_states)),
                                                          self.actions: np.vstack(np.array(self.episode_actions)),
                                                          self.discounted_episode_rewards_: discounted_episode_rewards
                                                          })
        self.episode_states, self.episode_actions, self.episode_rewards = [], [], []

    def append_sample(self,state, action, reward, next_state, done):
        action_procesed = np.zeros(self.action_size)
        action_procesed[action] = 1

        self.episode_actions.append(action_procesed)

        self.episode_rewards.append(reward)
        self.episode_states.append(state)
    def save_model(self):

        self.saver.save(self.sess, "./models/agent.ckpt")
        print("Model saved")

    def load_model(self,agent_to_load_directory):

        self.saver.restore(self.sess,  "./models/agent.ckpt")
    def train_model(self):
        pass





class AgentPGPong(BaseAgent):



    def __init__(self, state_size, action_size, agent_settings, is_agent_to_load, game_name):
        super().__init__(state_size, action_size, agent_settings, is_agent_to_load, game_name)
        self.learning_rate=agent_settings.learning_rate

        self.batch_state_action_reward_tuples=[]
        self.episode_number=0

        self.before_state=None
        self.is_first=True
        ## ENVIRONMENT Hyperparameters
        self.state_size = state_size
        self.action_size = action_size

        ## TRAINING Hyperparameters
        # max_episodes = 3000

        self.gamma = agent_settings.gamma  # Discount rate
        self.episode_states, self.episode_actions, self.episode_rewards = [], [], []
        self.is_baseline = False
        self.build_model()
        self.saver = tf.train.Saver()
        # if is_agent_to_load:
        #     self.load_model(agent_to_load_directory)

    def build_model(self):

        # set TensorFlow Session
        self.sess = tf.InteractiveSession()
        # set observations
        self.observations = tf.placeholder(tf.float32, [None, 6400])
        # set actions: +1 for up, -1 for down
        self.sampled_actions = tf.placeholder(tf.float32, [None, 1])
        self.advantage = tf.placeholder(tf.float32, [None, 1], name='advantage')
        # hidden layers features
        hidden_layers = tf.layers.dense(self.observations, units=200, activation=tf.nn.relu,
                                        kernel_initializer=tf.contrib.layers.xavier_initializer())
        self.up_probability = tf.layers.dense(hidden_layers, units=1, activation=tf.sigmoid,
                                              kernel_initializer=tf.contrib.layers.xavier_initializer())
        self.loss = tf.losses.log_loss(labels=self.sampled_actions, predictions=self.up_probability,
                                       weights=self.advantage)
        # set optimizer of network
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.train_op = optimizer.minimize(self.loss)

        tf.global_variables_initializer().run()
        self.saver = tf.train.Saver()

    def append_sample(self, state, action, reward, next_state, done):
        UP_ACTION = 2
        DOWN_ACTION = 3
        action_dict = {DOWN_ACTION: 0, UP_ACTION: 1}
        state=self.preprocess(state)
        next_state=self.preprocess(next_state)
        observation_delta = next_state - state
        tup = (observation_delta, action_dict[action], reward)
        self.batch_state_action_reward_tuples.append(tup)

    def get_action(self, state):
        UP_ACTION = 2
        DOWN_ACTION = 3
        state=self.preprocess(state)
        if self.is_first:
            self.before_state=state
            self.is_first=False
            return UP_ACTION
        else:
            observation_delta = state - self.before_state
            self.before_state=state

        up_probability = self.sess.run(self.up_probability, feed_dict={self.observations: observation_delta.reshape([1, -1])})[0]
        if np.random.uniform() < up_probability:
            action = UP_ACTION
        else:
            action = DOWN_ACTION
        return action

    def train_model(self):


        states, actions, rewards = zip(*self.batch_state_action_reward_tuples)
        rewards = self.discount_rewards(rewards, self.gamma)
        rewards = rewards - np.mean(rewards)
        rewards = rewards / np.std(rewards)
        batch_state_action_reward_tuples = list(zip(states, actions, rewards))
        self.train(batch_state_action_reward_tuples)
        self.batch_state_action_reward_tuples = []

    def discount_rewards(self,rewards, discount_factor):
        discounted_rewards = np.zeros_like(rewards)
        for t in range(len(rewards)):
            discounted_reward_sum = 0
            discount = 1
            for k in range(t, len(rewards)):
                discounted_reward_sum += rewards[k] * discount
                discount *= discount_factor
                if rewards[k] != 0:
                    # Don't count rewards from subsequent rounds
                    break
            discounted_rewards[t] = discounted_reward_sum
        return discounted_rewards

    def train(self, state_action_reward_tuples):
        states, actions, rewards = zip(*state_action_reward_tuples)
        # stack together  states, actions, and rewards for this episode
        states = np.vstack(states)
        actions = np.vstack(actions)
        rewards = np.vstack(rewards)

        feed_dict = {self.observations: states, self.sampled_actions: actions, self.advantage: rewards}
        self.sess.run(self.train_op, feed_dict)


    def preprocess(self,I):
        """ prepro 210x160x3 uint8 frame into 6400 (80x80) 1D float vector """
        I = I[35:195]  # crop
        I = I[::2, ::2, 0]  # downsample by factor of 2
        I[I == 144] = 0  # erase background (background type 1)
        I[I == 109] = 0  # erase background (background type 2)
        I[I != 0] = 1  # everything else (paddles, ball) just set to 1
        return I.astype(np.float).ravel()

    def save_model(self,file_name="./models/agentPPO"):
        self.saver.save(self.sess, file_name)

    def load_model(self, agent_to_load_directory):
        self.saver.restore(self.sess, agent_to_load_directory)









