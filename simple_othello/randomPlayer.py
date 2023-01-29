#!/usr/bin/env python
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from agent import Agent

class PlayerRandom(Agent):

    def get_pos(self):
        # board = self.env.state

        legal_actions = self.env.get_legal_actions()
        if len(legal_actions) == 0:
            action = self.CFG.pass_
        else:
            action = self.select(legal_actions)

        return action  # Randome

    def select(self, legal_actions):
        idx = random.randrange(len(legal_actions))
        return legal_actions[idx]
        

