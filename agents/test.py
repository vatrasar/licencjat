from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.common.vec_env import VecFrameStack
from stable_baselines import A2C
import gym
import numpy as np
from stable_baselines.common.policies import CnnLstmPolicy
from stable_baselines.common.policies import CnnPolicy

def callback(_locals, _globals):


    time_steps=_locals['update']*_locals['runner'].n_steps*_locals['runner'].env.num_envs
    print(time_steps)

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

    def close(self):
        # self.env.venv.envs[0].unwrapped.viewer.window.close()
        self.env.envs[0].unwrapped.viewer.window.close()



# There already exists an environment generator
# that will make and wrap atari environments correctly.
# Here we are also multiprocessing training (num_env=4 => 4 processes)
env = make_atari_env("AssaultNoFrameskip-v4", num_env=16, seed=0)

# # Frame-stacking withgoogle 4 frames
import time
model = A2C (CnnLstmPolicy, env, verbose=1)
model.learn(total_timesteps=500,callback=callback)
env = TestEnv("AssaultNoFrameskip-v4",16)
obs = env.reset()
score=0
while True:

    action, _states = model.predict(obs)

    obs, rewards, dones, info = env.step(action)
    score+=rewards
    if rewards!=0:
        print(score)
        time.sleep(5)
    if dones==True:
        score=0

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