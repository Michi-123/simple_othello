#!/usr/bin/env python
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import copy

class Othello:

    def __init__(self, CFG):

        self.CFG = CFG
        self.state = None
        self.player = None
        self.pass_counter = None
        self.change_pos_list = []
        self.search_directions = self._get_search_directions(CFG)
        self.max_range_index = self._get_max_range_index(CFG)

    def _get_search_directions(self, CFG):
        """ 
        探索ポイント（8方向）
        [-6, -5, -4, -1, 1, 4, 5, 6]
        """
        c = CFG.lines

        return [-c-2, -c-1, -c, -1, 1, c, c+1, c+2]


    def _get_max_range_index(self, CFG):
        """ 
        壁を含んだ最大インデックス
        """
        c = CFG.lines
        return c * c + c - 1

    def reset(self):
        self.player=self.CFG.first_player
        self.pass_counter = 0
        self.change_pos_list
        self._set_init_state()
        return self.state

    def _set_init_state(self):
        state = []
        for i in range(self.CFG.action_size):
            state.append(self.CFG.blank)
            
        # 初期ピース
        state[27] = 1
        state[28] = -1
        state[35] = -1
        state[36] = 1
        self.state = state

    def step(self, action):
        reward = 0
        done = False


        if self._is_done():
            done = True
            self.done = True
            print("player", self.player)
            
            if not self._is_draw():
                reward = -1
            
            return self.state, reward, done

        if action == self.CFG.pass_:
            print("Pass");input("Wait...")
            self.player = -self.player
            return self.state, reward, done

        if not self._is_legal_action(action):
            input("E100..not legal action!....")
            return self.state, reward, done

        # change_pos_list = self.get_change_pos_list(action)

        for pos in self.change_pos_list:
            self.state[pos] = self.player

        next_state = self._get_next_state(action)
        self.state = next_state

        # if self._is_done():
        #     done = True
 
        #     if not self._is_draw():
        #         reward = -1
            
        #     return next_state, reward, done
            
        self.player = -self.player
        return next_state, reward, done

    def render(self, plt=None):
        state = np.array(self.state).reshape(self.CFG.lines, -1)

        if plt==True:
            # print(state)
            self.draw_board()
        else:
            print(state)

    def _get_next_state(self, action):
        next_state=copy.deepcopy(self.state)
        next_state[action] = self.player
        return next_state

    def _is_done(self):
        for s in self.state:
            if s == 0:
                return False
        
        return True

    def count_winner(self, player):
        w = 0
        b = 0
        for s in self.state:
            if s == -1:
                b += 1
            elif s == 1:
                w += 1
        print("black", b)
        print("white", w)
        if b < w:
            reward = player
        else:
            reward = -player

        return reward
 
    def _is_draw(self):
        return False

    def _is_legal_action(self, action):

        # 壁の追加（戻り値：壁付の盤面と、位置情報）
        board, pos = self._add_wall(action)

        is_legal_action = False
        
        # 探索ポイント別に処理（線形探索）
        self.change_pos_list = []
        for search_direction in self.search_directions:

            # 探索ポイントを設定
            search_pos = pos + search_direction

            # 盤面にないインデックスならスキップ
            if search_pos < 0 or search_pos > self.max_range_index:
                continue

            num_opponent = self._linear_search(search_direction, board, search_pos)

            if num_opponent > 0:
                is_legal_action = True
                # 反転させた位置を格納
                self._set_change_pos(pos, search_direction, num_opponent)

        return is_legal_action

    def _linear_search(self, search_direction, board, search_pos):
        # 相手の駒のカウント初期化
        num_opponent = 0

        # 置き石である間繰り返し
        while True:

            # 相手の石なら
            if board[search_pos] == -self.player:
                num_opponent += 1
                search_pos = search_pos + search_direction
                # 範囲外のインデックスなら跳ばす
                if search_pos < 0 or self.max_range_index < search_pos:
                    is_search_end_point = False
                    break
            # 自分の石なら
            elif board[search_pos] == self.player:
                is_search_end_point = True
                break
            else:
                is_search_end_point = False
                break
        
        if not is_search_end_point:
            num_opponent = 0

        return num_opponent


    def get_legal_actions(self):

        legal_actions = []

        for action in range(64):
            if self.state[action] == 0:
                if self._is_legal_action(action):
                    legal_actions.append(action)
        
        return legal_actions
   
    def _add_wall(self, action):
        state = self.state
        board = []
        pos = action

        for i in range(len(state)):
            if i % self.CFG.lines == 0:
                board.append(self.CFG.wall)
                board.append(state[i])
                if i <= action:
                    pos += 1
            else:
                board.append(state[i])

        return board, pos

    def _set_change_pos(self, pos, search_direction, num_opponent):

        # 検索ポイントを初期化
        search_pos = pos + search_direction

        # 変更箇所を一覧に追加
        temp_change_pos_list = []
        for i in range(num_opponent):
            temp_change_pos_list.append(search_pos)
            search_pos = search_pos + search_direction

        # 補正
        # Remove Wall positiojn
        for i, pos in enumerate(temp_change_pos_list):

            if 1 <= pos <= 8:
                temp_change_pos_list[i] -= 1
            elif 10 <= pos <= 17:
                temp_change_pos_list[i] -= 2
            elif 19 <= pos <= 26:
                temp_change_pos_list[i] -= 3
            elif 28 <= pos <= 35:
                temp_change_pos_list[i] -= 4
            elif 37 <= pos <= 44:
                temp_change_pos_list[i] -= 5
            elif 46 <= pos <= 53:
                temp_change_pos_list[i] -= 6
            elif 55 <= pos <= 62:
                temp_change_pos_list[i] -= 7
            elif 64 <= pos <= 71:
                temp_change_pos_list[i] -= 8

        
        for pos in temp_change_pos_list:
            self.change_pos_list.append(pos)

        # for pos in self.change_pos_list:
        #     self.state[pos] = self.player


    def draw_board(self):
        # https://qiita.com/secang0/items/1229212a37d8c9922901

        img_gray = []
        img = []
        counter = 1

        for i in self.state:
            if i == 1:
                j = [255, 255, 255] # white
            elif i == -1:
                j = [0, 0, 0] # Black
            else:
                j = [0, 150, 0] # Green

            img.append(j)
            if counter % self.CFG.lines == 0:
                img_gray.append(img)
                img = []
            counter += 1

        img_gray = np.array(img_gray, dtype=np.uint8)

        # Figureを設定
        fig = plt.figure()
        # Axesを追加
        ax = fig.add_subplot(111)        
        # x軸の目盛設定
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8])

        plt.grid(color='b', linestyle=':', linewidth=0.3)
        plt.imshow(img_gray, cmap='gray_r', vmin=0, vmax=100, interpolation='none')
        # plt.imshow(img_gray, cmap='gray_r', vmin=0, vmax=255, interpolation='none')
        plt.show()

        # timestamp = int(time.time() * 1000)
        # filename = "save\picture_" + str(timestamp) + ".png"
        # plt.imsave(filename, img_gray, vmin=0, vmax=255, cmap='gray_r', format='png', origin='upper', dpi=0.01)
        
        # self.save_log(board, pos)