#!/usr/bin/env python3

import random
import keyboard
import copy
import sys
import os
import time
import threading


class GameField:
    symbols = ["╔", "╗", "╚", "╝", "═", "║", " ", "█"]

    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.game_matrix = [[0 for i in range(width)] for j in range(height)]

    def __str__(self):
        res = self.symbols[0] + self.symbols[4] * \
            self.width + self.symbols[1] + "\n"
        for row in self.game_matrix:
            res += self.symbols[5]
            for el in row:
                res += self.symbols[6 + el]
            res += self.symbols[5] + "\n"
        res += self.symbols[2] + self.symbols[4] * \
            self.width + self.symbols[3] + "\n"
        return res

    def copy(self):
        return copy.deepcopy(self)

    def clear(self):
        self.game_matrix = [[0 for i in range(self.width)] for j in range(self.height)]

    def remove_row(self, n):
        self.game_matrix.pop(n)
        self.game_matrix.insert(0, [0 for i in range(self.width)])


class Shape:
    symbol = "█"
    x = 0
    y = 0

    def __init__(self, height, width, state = 0):
        self.height = height
        self.width = width
        self.state = state

        self.game_matrix = [[0 for i in range(width)] for j in range(height)]

    def __str__(self):
        res = ""
        for row in self.game_matrix:
            for el in row:
                res += self.symbol if el == 1 else " "
            res += "\n"
        return res

    def copy(self):
        return copy.deepcopy(self)

    def move_left(self, gamefield: GameField):
        if self.x == 0:
            return False

        c = self.copy()
        c.x -= 1

        if c.intersection(gamefield):
            return False

        self.x -= 1
        return True

    def move_right(self, gamefield: GameField):
        if self.x + self.width == gamefield.width:
            return False

        c = self.copy()
        c.x += 1

        if c.intersection(gamefield):
            return False

        self.x += 1
        return True

    def move_down(self, gamefield: GameField):
        if self.y + self.height == gamefield.height:
            return False

        c = self.copy()
        c.y += 1

        if c.intersection(gamefield):
            return False
        
        self.y += 1
        return True

    def rotate(self, gamefield: GameField):
        c = self.copy()
        c.__init__((self.state + 1) % 4)
        if c.x + c.width < gamefield.width and not c.intersection(gamefield):
            self.__init__((self.state + 1) % 4)

    def add_place(self, gamefield: GameField):
        for i in range(self.height):
            for j in range(self.width):
                if i + self.y >= 0:
                    gamefield.game_matrix[i + self.y][j + self.x] += self.game_matrix[i][j]
    
    def intersection(self, gamefield: GameField):
        for i in range(self.height):
            for j in range(self.width):
                if max(i+self.y, 0) >= gamefield.height or j + self.x >= gamefield.width:
                    return True
                if self.game_matrix[i][j] == 1 and gamefield.game_matrix[max(i+self.y, 0)][j+self.x] == 1:
                    return True
        return False


class SShape(Shape):
    def __init__(self, state = 0):
        if state == 0 or state == 2:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][1] = 1
            self.game_matrix[0][2] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
        elif state == 1 or state == 3:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[2][1] = 1


class SShape_rev(Shape):
    def __init__(self, state = 0):
        if state == 0 or state == 2:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[0][1] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[1][2] = 1
        elif state == 1 or state == 3:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][1] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[2][0] = 1


class OShape(Shape):
    def __init__(self, state = 0):
        Shape.__init__(self, 2, 2, state)
        self.game_matrix[0][0] = 1
        self.game_matrix[0][1] = 1
        self.game_matrix[1][0] = 1
        self.game_matrix[1][1] = 1


class LShape(Shape):
    def __init__(self, state = 0):
        if state == 0:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[2][0] = 1
            self.game_matrix[2][1] = 1
        elif state == 1:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[0][1] = 1
            self.game_matrix[0][2] = 1
            self.game_matrix[1][0] = 1
        elif state == 2:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[0][1] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[2][1] = 1
        elif state == 3:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][2] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[1][2] = 1


class LShape_rev(Shape):
    def __init__(self, state = 0):
        if state == 0:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][1] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[2][1] = 1
            self.game_matrix[2][0] = 1
        elif state == 1:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[1][2] = 1
        elif state == 2:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[0][1] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[2][0] = 1
        elif state == 3:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[0][1] = 1
            self.game_matrix[0][2] = 1
            self.game_matrix[1][2] = 1


class TShape(Shape):
    def __init__(self, state = 0):
        if state == 0:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][1] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[1][2] = 1
        elif state == 1:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[2][0] = 1
        elif state == 2:
            Shape.__init__(self, 2, 3, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[0][1] = 1
            self.game_matrix[0][2] = 1
            self.game_matrix[1][1] = 1
        elif state == 3:
            Shape.__init__(self, 3, 2, state)
            self.game_matrix[0][1] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[1][1] = 1
            self.game_matrix[2][1] = 1


class IShape(Shape):
    def __init__(self, state = 0):
        if state == 0 or state == 2:
            Shape.__init__(self, 4, 1, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[1][0] = 1
            self.game_matrix[2][0] = 1
            self.game_matrix[3][0] = 1
        elif state == 1 or state == 3:
            Shape.__init__(self, 1, 4, state)
            self.game_matrix[0][0] = 1
            self.game_matrix[0][1] = 1
            self.game_matrix[0][2] = 1
            self.game_matrix[0][3] = 1


def create_shape(n):
    if n == 0:
        return TShape()
    if n == 1:
        return SShape()
    if n == 2:
        return OShape()
    if n == 3:
        return LShape()
    if n == 4:
        return SShape_rev()
    if n == 5:
        return LShape_rev()
    if n == 6:
        return IShape()


class Game:
    def __init__(self, height, width):
        self.gamefield = GameField(height, width)
        self.shape = create_shape(random.randint(0, 6))
        self.isgameover = False
        self.score = 0
        self.lock = threading.RLock()

    def __str__(self):
        with self.lock:
            gf = self.gamefield.copy()
            self.shape.add_place(gf)
            return str(gf)

    def next_tick(self):
        with self.lock:
            d = self.shape.move_down(self.gamefield)
            if not d:
                self.shape.add_place(self.gamefield)
                self.remove_full_row()
                new_shape = create_shape(random.randint(0, 6))
                
                flag = False
                while new_shape.intersection(self.gamefield) and new_shape.y + new_shape.height >= 0:
                    flag = True
                    new_shape.y -= 1

                if flag:
                    self.isgameover = True

                self.shape = new_shape
            return d

    def move_left(self):
        with self.lock:
            return self.shape.move_left(self.gamefield)

    def move_right(self):
        with self.lock:
            x = self.shape.move_right(self.gamefield)
            return x

    def rotate(self):
        with self.lock:
            return self.shape.rotate(self.gamefield)

    def move_down(self):
        with self.lock:
            return self.shape.move_down(self.gamefield)

    def is_gameover(self):
        with self.lock:
            return self.isgameover or any(x == 1 for x in self.gamefield.game_matrix[0])

    def remove_full_row(self) -> bool:
        with self.lock:
            for i in range(self.gamefield.height):
                if all(x == 1 for x in self.gamefield.game_matrix[i]):
                    self.gamefield.remove_row(i)
                    self.score += 1

    def score_count(self):
        with self.lock:
            print(f'Your score: {self.score}')

    def handle_keyboard_input(self):
        with self.lock:
            keyboard.on_press_key('up', lambda _: game.rotate())
            keyboard.on_press_key('left', lambda _: self.move_left())
            keyboard.on_press_key('right', lambda _: self.move_right())
            keyboard.on_press_key('down', lambda _: self.move_down())

    def get_gamefield_with_shape(self):
        with self.lock:
            gmfld = self.gamefield.copy()
            self.shape.add_place(gmfld)
            return gmfld

if __name__ == '__main__':
    game = Game(20, 10)

    game.handle_keyboard_input()

    while True:

        os.system('clear')
        os.system('cls')
        
        game.score_count()

        print(game)
        sys.stdout.flush()
        time.sleep(1)

        if game.is_gameover():
            break

        game.next_tick()
