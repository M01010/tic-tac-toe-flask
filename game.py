from player import Player


class Game:

    def __init__(self):
        self.bot = Player.Min
        self.user = Player.Max
        self.matrix = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]

    def set_user(self, user):
        self.user = user
        self.matrix = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]
        if self.user == Player.Max:
            self.bot = Player.Min
        else:
            self.bot = Player.Max

    def evaluate(self) -> int:
        def check(x: str):
            for i in range(3):
                if self.matrix[i][0] == self.matrix[i][1] == self.matrix[i][2] == x:
                    return True
            for i in range(3):
                if self.matrix[0][i] == self.matrix[1][i] == self.matrix[2][i] == x:
                    return True
            if self.matrix[0][0] == self.matrix[1][1] == self.matrix[2][2] == x:
                return True
            if self.matrix[0][2] == self.matrix[1][1] == self.matrix[2][0] == x:
                return True
            return False

        if check(Player.Max.value):
            return 10
        if check(Player.Min.value):
            return -10
        return 0

    def terminal(self) -> bool:
        def check(x: str, y: str, z: str) -> bool:
            return x == y == z and x != ' '

        for i in range(3):
            if check(self.matrix[i][0], self.matrix[i][1], self.matrix[i][2]):
                return True
        for i in range(3):
            if check(self.matrix[0][i], self.matrix[1][i], self.matrix[2][i]):
                return True
        if check(self.matrix[0][0], self.matrix[1][1], self.matrix[2][2]):
            return True
        if check(self.matrix[0][2], self.matrix[1][1], self.matrix[2][0]):
            return True
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == ' ':
                    return False
        return True

    def maximize(self, depth=0) -> int:
        if self.terminal():
            return self.evaluate() + depth
        val = -999
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == ' ':
                    self.matrix[i][j] = Player.Max.value
                    val = max(val, self.minimize(depth + 1))
                    self.matrix[i][j] = ' '
                    if val == 10 - depth:
                        return val
        return val

    def minimize(self, depth=0) -> int:
        if self.terminal():
            return self.evaluate() - depth
        val = 999
        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == ' ':
                    self.matrix[i][j] = Player.Min.value
                    val = min(val, self.maximize(depth + 1))
                    self.matrix[i][j] = ' '
                    if val == 10 + depth:
                        return val
        return val

    def minimax(self):
        best_action = None
        if self.bot == Player.Max:
            highest = -999
            for i in range(3):
                for j in range(3):
                    if self.matrix[i][j] == ' ':
                        self.matrix[i][j] = self.bot.value
                        val = self.minimize()
                        self.matrix[i][j] = ' '
                        if val > highest:
                            highest = val
                            best_action = i, j
            self.matrix[best_action[0]][best_action[1]] = self.bot.value
            return
        else:
            lowest = 999
            for i in range(3):
                for j in range(3):
                    if self.matrix[i][j] == ' ':
                        self.matrix[i][j] = self.bot.value
                        val = self.maximize()
                        self.matrix[i][j] = ' '
                        if val < lowest:
                            lowest = val
                            best_action = i, j
            self.matrix[best_action[0]][best_action[1]] = self.bot.value
            return

    def play_user(self, i, j):
        try:
            if self.matrix[i][j] == ' ':
                self.matrix[i][j] = self.user.value
            else:
                raise Exception('chosen before')
        except Exception as e:
            raise e
