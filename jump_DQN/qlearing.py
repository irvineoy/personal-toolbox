# -*- coding:utf-8 -*-
# python

import cv2
from PIL import Image
import pandas as pd
import numpy as np
import jump_game_control as game

piece_base_height_1_2 = 28
piece_body_width = 110
PRESSTIME = [300, 500, 600, 700, 800, 900, 1000, 1100]


class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        # self.qTable = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.qTable = pd.read_csv('./data/q_table.csv', index_col=0, dtype=np.float64)

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < self.epsilon:
            state_action = self.qTable.loc[observation, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.argmax()
        else:
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.qTable.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.qTable.loc[s_, :].max()
        else:
            q_target = r
        self.qTable.loc[s, a] += self.lr * (q_target - q_predict)
        self.qTable.to_csv('./data/q_table.csv')
        print 'The reward is ', r
        print 'The situation is ', s
        print 'The action is ', a
        print self.qTable


    def check_state_exist(self, state):
        if state not in self.qTable.index:
            self.qTable = self.qTable.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.qTable.columns,
                    name=state,
                )
            )


def find_piece_and_board(im):
    """
    寻找关键坐标
    """
    im = Image.fromarray(im)
    w, h = im.size
    points = []  # 所有满足色素的点集合
    piece_y_max = 0
    board_x = 0
    board_y = 0
    scan_x_border = int(w / 8)  # 扫描棋子时的左右边界
    scan_start_y = 0  # 扫描的起始 y 坐标
    im_pixel = im.load()
    # 以 50px 步长，尝试探测 scan_start_y
    for i in range(int(h / 3), int(h * 2 / 3), 50):
        last_pixel = im_pixel[0, i]
        for j in range(1, w):
            pixel = im_pixel[j, i]
            # 不是纯色的线，则记录 scan_start_y 的值，准备跳出循环
            if pixel != last_pixel:
                scan_start_y = i - 50
                break
        if scan_start_y:
            break
    print('start scan Y axis: {}'.format(scan_start_y))

    # 从 scan_start_y 开始往下扫描，棋子应位于屏幕上半部分，这里暂定不超过 2/3
    for i in range(scan_start_y, int(h * 2 / 3)):
        # 横坐标方面也减少了一部分扫描开销
        for j in range(scan_x_border, w - scan_x_border):
            pixel = im_pixel[j, i]
            # 根据棋子的最低行的颜色判断，找最后一行那些点的平均值，这个颜
            # 色这样应该 OK，暂时不提出来
            if (50 < pixel[0] < 60) \
                    and (53 < pixel[1] < 63) \
                    and (95 < pixel[2] < 110):
                points.append((j, i))
                piece_y_max = max(i, piece_y_max)

    bottom_x = [x for x, y in points if y == piece_y_max]  # 所有最底层的点的横坐标
    if not bottom_x:
        return 0, 0, 0, 0, 0

    piece_x = int(sum(bottom_x) / len(bottom_x))  # 中间值
    piece_y = piece_y_max - piece_base_height_1_2  # 上移棋子底盘高度的一半

    # 限制棋盘扫描的横坐标，避免音符 bug
    if piece_x < w / 2:
        board_x_start = piece_x
        board_x_end = w
    else:
        board_x_start = 0
        board_x_end = piece_x

    for i in range(int(h / 3), int(h * 2 / 3)):
        last_pixel = im_pixel[0, i]
        if board_x or board_y:
            break
        board_x_sum = 0
        board_x_c = 0

        for j in range(int(board_x_start), int(board_x_end)):
            pixel = im_pixel[j, i]
            # 修掉脑袋比下一个小格子还高的情况的 bug
            if abs(j - piece_x) < piece_body_width:
                continue

            # 检查Y轴下面5个像素， 和背景色相同， 那么是干扰
            ver_pixel = im_pixel[j, i + 5]
            if abs(pixel[0] - last_pixel[0]) \
                    + abs(pixel[1] - last_pixel[1]) \
                    + abs(pixel[2] - last_pixel[2]) > 10 \
                    and abs(ver_pixel[0] - last_pixel[0]) \
                            + abs(ver_pixel[1] - last_pixel[1]) \
                            + abs(ver_pixel[2] - last_pixel[2]) > 10:
                board_x_sum += j
                board_x_c += 1
        if board_x_sum:
            board_x = board_x_sum / board_x_c
    last_pixel = im_pixel[board_x, i]

    # 首先找到游戏的对称中心，由对称中心做辅助线与x=board_x直线的交点即为棋盘的中心位置
    # 有了对称中心，可以知道棋子在棋盘上面的相对位置（偏高或偏低，偏高的话测量值比实际值大，
    # 偏低相反。最后通过delta_piece_y来对跳跃时间进行微调
    center_x = w / 2 + (24 / 1080) * w
    center_y = h / 2 + (17 / 1920) * h
    if piece_x > center_x:
        board_y = round((25.5 / 43.5) * (board_x - center_x) + center_y)
        delta_piece_y = piece_y - round((25.5 / 43.5) * (piece_x - center_x) + center_y)
    else:
        board_y = round(-(25.5 / 43.5) * (board_x - center_x) + center_y)
        delta_piece_y = piece_y - round(-(25.5 / 43.5) * (piece_x - center_x) + center_y)

    if not all((board_x, board_y)):
        return 0, 0, 0, 0, 0
    return piece_x, piece_y, board_x, board_y, delta_piece_y


def return_step(x1, y1, x2, y2): return round(((x1 - x2)**2 + (y1 - y2)**2)**0.5 / 50)


def run():
    # img = cv2.imread('./data/jump_temp.png')
    qlearning = QLearningTable(actions=list(range(8)), e_greedy=1.0)
    gamecl = game.GameState()
    img = gamecl.get_start()
    piece_x_, piece_y_, board_x_, board_y_, delta_piece_y_ = find_piece_and_board(img)

    for i in range(1000):
        piece_x, piece_y, board_x, board_y, delta_piece_y = piece_x_, piece_y_, board_x_, board_y_, delta_piece_y_
        action = qlearning.choose_action(return_step(piece_x, piece_y, board_x, board_y))
        image_data, reward, terminal = gamecl.frame_step(action, delta_piece_y)
        piece_x_, piece_y_, board_x_, board_y_, delta_piece_y_ = find_piece_and_board(image_data)
        qlearning.learn(return_step(piece_x, piece_y, board_x, board_y),
                        action,
                        reward - (delta_piece_y_/1000),
                        return_step(piece_x_, piece_y_, board_x_, board_y_))
        if i % 50 == 0:
            pass


if __name__ == '__main__':
    run()
