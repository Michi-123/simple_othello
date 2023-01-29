#!/usr/bin/env python
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from agent import Agent

class PlayerHuman(Agent):

    def get_pos(self):
        print("player", self.env.player)
        pos = input('(x,y):')

        if pos is None or pos == "":
            pos = 0
        else:
            pos = pos.replace('.', ',')
            pos = pos.split(',')
            pos = int(pos[0]) * self.CFG.lines + int(pos[1])
            print("pos", pos)
            # pos = int(pos)-1
        return pos

    @staticmethod
    def wrong_pos():
        print("Wrong position.")

    @staticmethod
    def game_over(score):
        pass
