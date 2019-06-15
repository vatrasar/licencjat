from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.common.vec_env import VecFrameStack
from stable_baselines import PPO2
import gym
import numpy as np
from stable_baselines.common.policies import CnnLstmPolicy

def callback(_locals, _globals):


    time_steps=_locals['update']*_locals['runner'].n_steps*_locals['runner'].env.num_envs

class TestEnv:


    def __init__(self,env_name,number_of_envs) -> None:

        self.env=make_atari_env(env_name, num_env=1, seed=0)
        self.number_of_envs=number_of_envs


    def reset(self):
        obs = self.env.reset()
        return self.preproces_state(obs)

    def step(self,action):

        action=[action[0]]

        obs, rewards, dones, info=self.env.step(action)

        return self.preproces_state(obs),rewards[0],dones[0],[]



    def preproces_state(self,state):
        stack=[]
        new_state=state.tolist()
        new_state=new_state[0]

        for i in range(0,self.number_of_envs):
            stack.append(new_state)
        new_state=np.asarray(stack)
        return new_state
    def render(self):
        self.env.render()


# There already exists an environment generator
# that will make and wrap atari environments correctly.
# Here we are also multiprocessing training (num_env=4 => 4 processes)
env = make_atari_env('PongNoFrameskip-v4', num_env=8, seed=0)
# # Frame-stacking with 4 frames

#
model = PPO2(CnnLstmPolicy, env, verbose=1)
model.learn(total_timesteps=320,callback=callback)
env = TestEnv('PongNoFrameskip-v4',8)
obs = env.reset()
while True:

    action, _states = model.predict(obs)

    obs, rewards, dones, info = env.step(action)
    env.render()

#
# from stable_baselines.common.policies import MlpPolicy
# from stable_baselines.common.vec_env import SubprocVecEnv
# from stable_baselines import PPO2
#
# # multiprocess environment
# n_cpu = 4
# env = SubprocVecEnv([lambda: gym.make('CartPole-v1') for i in range(n_cpu)])
#
# model = PPO2(MlpPolicy, env, verbose=1)
# model.learn(total_timesteps=25000,callback=callback)
# model.save("ppo2_cartpole")
#
# del model # remove to demonstrate saving and loading
#
# model = PPO2.load("ppo2_cartpole")
#
# # Enjoy trained agent
# obs = env.reset()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()