#!/usr/bin/env python

import gymnasium as gym
import pathery_env
from pathery_env.wrappers.action_mask_observation import ActionMaskObservationWrapper
from pathery_env.wrappers.convolution_observation import ConvolutionObservationWrapper
from enum import Enum
import numpy as np

mapString = '13.6.8.Simple...1725768000:,r3.1,c1.9,r3.,r3.1,r1.3,r1.5,r3.,r3.1,r1.6,r1.2,r3.,r3.2,r1.8,r3.,s1.4,r1.6,r3.,r3.7,r1.3,f1.'

def isWrappedBy(env, wrapper_type):
  """Recursively unwrap env to check if any wrapper is of type wrapper_type."""
  current_env = env
  while isinstance(current_env, gym.Wrapper):
    if isinstance(current_env, wrapper_type):
      return True
    current_env = current_env.env  # Unwrap to the next level
  return False

if __name__ == "__main__":
  # env = gym.make('pathery_env/Pathery-RandomNormal', render_mode='ansi')
  env = gym.make('pathery_env/Pathery-FromMapString', render_mode='ansi', map_string=mapString)
  env = ActionMaskObservationWrapper(env)
  env = ConvolutionObservationWrapper(env)

  while True:
    obs, info = env.reset()
    done = False

    print(f'Start; {info}')
    if isWrappedBy(env, ActionMaskObservationWrapper):
      print(f'Mask; {obs["action_mask"]}')

    def readPair():
      user_input = input("Enter two integers separated by space: ")
      num1, num2 = user_input.split()
      return (int(num1), int(num2))

    while not done:
      print(env.render())
      pairInput = readPair()
      while pairInput not in env.action_space:
        print('invalid action')
        pairInput = readPair()
      observation, reward, done, _, info = env.step(pairInput)
      print(f'Reward: {reward}, info: "{info}"')
      if done:
        print(env.render())
        print(f'\n{"~"*20}End of episode{"~"*20}\n')
