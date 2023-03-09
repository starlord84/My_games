from random import randint


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.__computer_count = self.__user_count = 0
        self._size = 3
        self.pole = tuple(tuple(Cell() for _ in range(self._size)) for _ in range(self._size))
        self._win = 0

    def __check_indx_tuple(self, item):
        if type(item) != tuple or len(item) != 2:
            raise IndexError('некорректно указанные индексы')
        for indx in item:
            if type(indx) != int or not (0 <= indx < self._size):
                raise IndexError('некорректно указанные индексы')

    def __getitem__(self, item):
        self.__check_indx_tuple(item)
        row, col = item
        return self.pole[row][col].value

    def __update_win_status(self):
        for row in self.pole:
            if all(x.value == self.HUMAN_X for x in row):
                self._win = 1
                return

            if all(x.value == self.COMPUTER_O for x in row):
                self._win = 2
                return

        for i in range(self._size):
            if all(row[i].value == self.HUMAN_X for row in self.pole):
                self._win = 1
                return

            if all(row[i].value == self.COMPUTER_O for row in self.pole):
                self._win = 2
                return

        if all(self.pole[i][i].value == self.HUMAN_X for i in range(self._size)) or \
            all(self.pole[i][-1 - i].value == self.HUMAN_X for i in range(self._size)):
            self._win = 1
            return

        if all(self.pole[i][i].value == self.COMPUTER_O for i in range(self._size)) or \
            all(self.pole[i][-1 - i].value == self.COMPUTER_O for i in range(self._size)):
            self._win = 2
            return

        if all(x.value != self.FREE_CELL for row in self.pole for x in row):
            self._win = 3
            return

    def __setitem__(self, key, value):
        row, col = key
        self.__check_indx_tuple(key)
        if self.pole[row][col]:
            self.pole[row][col].value = value
            self.__user_count = 0
            self.__update_win_status()
        else:
            print('Клетка уже занята')
            self.__user_count += 1
            return self.human_go()

    def init(self):
        for row in self.pole:
            for cell in row:
                cell.value = self.FREE_CELL
        self._win = 0

    def show(self):
        for row in self.pole:
            print(*map(lambda x: '#' if x.value == 0 else x.value, row))
        print('------------------------')

    def human_go(self):
        print('Твой ход' if self.__user_count == 0 else 'Повтори ход')
        key = tuple(map(int, input('Введи два целых числа через пробел: ').split()))
        self.__setitem__(key, self.HUMAN_X)

    def computer_go(self):
        print('Ход бомжа' if self.__computer_count == 0 else 'Бомж ошибся')
        row, col = randint(0, self._size - 1), randint(0, self._size - 1)
        if self.pole[row][col]:
            self.__setitem__((row, col), self.COMPUTER_O)
            self.__computer_count = 0
        else:
            self.__computer_count += 1
            return self.computer_go()

    def __bool__(self):
        return self._win == 0 and self._win not in (1, 2, 3)

    @property
    def is_human_win(self):
        return self._win == 1

    @property
    def is_computer_win(self):
        return self._win == 2

    @property
    def is_draw(self):
        return self._win == 3
