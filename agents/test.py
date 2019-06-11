from stable_baselines.common.cmd_util import make_atari_env
from stable_baselines.common.vec_env import VecFrameStack
from stable_baselines import PPO2


def callback(_locals, _globals):


    return True


# There already exists an environment generator
# that will make and wrap atari environments correctly.
# Here we are also multiprocessing training (num_env=4 => 4 processes)
env = make_atari_env('BankHeistNoFrameskip-v4', num_env=8, seed=0)
# Frame-stacking with 4 frames
env = VecFrameStack(env, n_stack=4)

model = PPO2('CnnPolicy', env, verbose=1,cliprange=0.2)
model.learn(total_timesteps=3000000,callback=callback)

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()