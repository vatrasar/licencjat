import tensorflow as tf
import numpy as np
import gym
from settings import Settings

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
        saver = tf.train.Saver()
        saver.save(self.sess, "./models/agent.ckpt")
        print("Model saved")
    def load_model(self,agent_to_load_directory):
        saver = tf.train.Saver()
        saver.restore(self.sess,  "./models/agent.ckpt")
    def train_model(self):
        pass





