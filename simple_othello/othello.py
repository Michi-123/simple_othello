#!/usr/bin/env python
"""
オセロは、相手の手番で自分が勝つこともあるので、終了の報酬の値が五目並べとことなります
このプログラムコードは、ChatGPTに作らせたオセロをチューニングしたものです。
https://youtu.be/7OAXOu1HNkQ
"""

#version 1.x

def _is_on_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def _flip_pieces(state, player, xstart, ystart):
    state[xstart][ystart] = player
    search_directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    
    for xdir, ydir in search_directions:
        x, y = xstart + xdir, ystart + ydir
        
        if _is_on_board(x, y) and state[x][y] == -player:
            x += xdir
            y += ydir
            
            if not _is_on_board(x, y):
                continue
                
            while state[x][y] == -player:
                x += xdir
                y += ydir
                if not _is_on_board(x, y):
                    break
                    
            if not _is_on_board(x, y):
                continue
                
            if state[x][y] == player:
                while True:
                    x -= xdir
                    y -= ydir
                    if x == xstart and y == ystart:
                        break
                    state[x][y] = player


def _is_valid_move(state, player, x_start, y_start):
    if state[x_start][y_start] != 0:
        return False

    state[x_start][y_start] = player
    for x_dir, y_dir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = x_start + x_dir, y_start + y_dir

        if _is_on_board(x, y) and state[x][y] == -player:
            x += x_dir
            y += y_dir

            if not _is_on_board(x, y):
                continue
                
            while state[x][y] == -player:
                x += x_dir
                y += y_dir
                if not _is_on_board(x, y):
                    break

            if not _is_on_board(x, y):
                continue

            if state[x][y] == player:
                state[x_start][y_start] = 0
                return True

    state[x_start][y_start] = 0
    return False

# GPT Othello
class Othello:
    def __init__(self, CFG):
        self.CFG = CFG
        self.player = None
        self.state = None
        self.lines = 8 # 8x8 size board
        self.pass_player = {}

    def reset(self):
        self.state = [[0 for _ in range(8)] for _ in range(8)]
        self.state[3][3] = -1 # first_player
        self.state[4][4] = -1
        self.state[3][4] = 1 # second_player
        self.state[4][3] = 1
        self.player = self.CFG.first_player
        self.pass_player[self.CFG.first_player] = 0
        self.pass_player[self.CFG.second_player] = 0
        return self.state

    def step(self, a):

        if a == self.CFG.pass_:
            # パスのカウントアップ
            self.pass_player[self.player] += 1
            # パスが指定の値以上であれば負けとして終了
            if self.pass_player[self.player] > 1:
                return self.state, -1, True

            self.player = -self.player
            return self.state, 0, False

        x, y = a // 8, a % 8

        _flip_pieces(self.state, self.player, x, y)
        self.player = -self.player

        done = self.game_over()

        if done:
            reward = self.winner()
        else:
            reward = 0

        return self.state, reward, done

    def get_legal_actions(self):
        legal_actions = []
        for x in range(8):
            for y in range(8):
                if _is_valid_move(self.state, self.player, x, y):
                    legal_actions.append(x * 8 + y)
        return legal_actions

    def render(self):
        symbols = {1: 'O', 0: '-', -1: 'X'}
        print('  0 1 2 3 4 5 6 7')
        for i, row in enumerate(self.state):
            print(i, ' '.join(symbols[x] for x in row))

    def game_over(self):
        for row in self.state:
            if 0 in row:
                return False
        return True

    # def _is_pass(self):
    #     return not any(self.get_legal_actions())

    def winner(self):
        x_count = sum(row.count(-1) for row in self.state)
        o_count = sum(row.count(1) for row in self.state)

        if o_count < x_count:
            return -1
        elif x_count < o_count:
            return 1
        else:
            return 0
