#!/usr/bin/env python
import random
import time
import numpy as np
import matplotlib.pyplot as plt

from config import CFG
from othello import Othello
from randomPlayer import PlayerRandom
from humanPlayer import PlayerHuman

env = Othello(CFG)

#player1 = PlayerHuman(CFG, env)
player1 = PlayerRandom(CFG, env)
player2 = PlayerRandom(CFG, env)

plot=CFG.plot

env.reset()
# env.render(plt=plot)

while True:
    action = player1.get_pos()
    state, reward, done = env.step(action)
    env.render(plt=plot)
    if done:

        print("white win", reward)
        break

    action = player2.get_pos()
    state, reward, done = env.step(action)
    # env.render(plt=plot)
    if done:
        print("black win", reward)
        break

reward = env.count_winner(CFG.first_player)
print("reward", reward)
env.render(plt=plot)
