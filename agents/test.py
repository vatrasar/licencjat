from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.common.vec_env import VecFrameStack
from stable_baselines import PPO2
import gym
from stable_baselines.common.policies import CnnLstmPolicy

def callback(_locals, _globals):


    time_steps=_locals['update']*_locals['runner'].n_steps*_locals['runner'].env.num_envs



# There already exists an environment generator
# that will make and wrap atari environments correctly.
# Here we are also multiprocessing training (num_env=4 => 4 processes)
env = make_atari_env('PongNoFrameskip-v4', num_env=8, seed=0)
# # Frame-stacking with 4 frames

#
model = PPO2(CnnLstmPolicy, env, verbose=1)
model.learn(total_timesteps=320,callback=callback)

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render(mode='human')

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