from random import randint, shuffle


class Ship:
    def __init__(self, length, tp=1, x=None, y=None, is_move=True):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = is_move
        self._cells = [1] * length

    def set_start_coords(self, x, y):
        self._x, self._y = x, y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._is_move:
            if self._tp == 1:
                if go:
                    self._x = self._x + 1
                else:
                    self._x = self._x - 1
            else:
                if go:
                    self._y = self._y + 1
                else:
                    self._y = self._y - 1


    def is_collide(self, ship):
        if self._x is None:
            return False

        size = max(self._x, self._y, ship._x, ship._y) + max(self._length, ship._length) + 1
        pole = [[0 for _ in range(size)] for _ in range(size)]
        x, y, tp, length = self._x, self._y, self._tp, self._length
        if tp == 1:
            for i in range(length):
                pole[y][x + i] = self._cells[i]
        else:
            for i in range(length):
                pole[y + i][x] = self._cells[i]

        sx, sy, stp, slength = ship._x, ship._y, ship._tp, ship._length
        if stp == 1:
            for row in pole[(0, sy - 1)[sy - 1 > 0]:sy + 2]:
                sl = row[(0, sx - 1)[sx - 1 > 0]:(sx + slength + 1)]
                if 1 in sl or 2 in sl:
                    return True
        else:
            for row in pole[(0, sy - 1)[sy - 1 > 0]:sy + slength + 1]:
                sl = row[(0, sx - 1)[sx - 1 > 0]:(sx + 2)]
                if 1 in sl or 2 in sl:
                    return True
        return False

    def is_out_pole(self, size):
        if self._tp == 1:
            if (not 0 <= (self._x + self._length - 1) < size) or (not 0 <= self._y < size):
                return True
        else:
            if (not 0 <= (self._y + self._length - 1) < size) or (not 0 <= self._x < size):
                return True
        return False

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size=10):
        if size == 8:
            size = 10  # 10!
        self._size = size
        self._ships = []

    def init(self):
        self.get_pole(new=True)
        self._ships = []
        self._ships.reverse()
        [self._ships.append(Ship(i, tp=randint(1, 2))) for i in range(1, 5) for _ in range(5-i)]
        self.ship1_ship2()


    def ship1_ship2(self):
        for ship_1 in self._ships:
            add = True
            while add:
                x, y = randint(0, self._size - 1), randint(0, self._size - 1)
                tmp_ship = Ship(ship_1._length, randint(1, 2), x, y)
                if not tmp_ship.is_out_pole(self._size):
                    g = True
                    for a_ship in self._ships:
                        if a_ship.is_collide(tmp_ship):
                            g = False
                    if g:
                        ship_1.set_start_coords(x, y)
                        ship_1._tp = tmp_ship._tp
                        self.refresh_pole(ship_1)
                        add = False

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for ship_move in self._ships:
            xc, yc = ship_move._x, ship_move._y
            go = [-1, 1]
            shuffle(go)
            move = True
            for i in range(2):
                ship_move._x, ship_move._y = xc, yc
                ship_move.move(go[i])
                for ship_check in self._ships:
                    if ship_move != ship_check:
                        if ship_move.is_out_pole(self._size) or ship_check.is_collide(ship_move):
                            move = False
                            break
                if not move:
                    ship_move._x, ship_move._y = xc, yc
                else:
                    break

    def refresh_pole(self, ship):
        x, y, tp, length = ship._x, ship._y, ship._tp, ship._length
        if tp == 1:
            for i in range(length):
                self._pole[y][x + i] = ship._cells[i]
        else:
            for i in range(length):
                self._pole[y + i][x] = ship._cells[i]

    def show(self):
        self.get_pole(new=True)

        for ship in self._ships:
            self.refresh_pole(ship)

        for row in self._pole:
            print(*row)

    def get_pole(self, new=False):
        if not hasattr(self, '_pole') or new:
            self._pole = [[0 for _ in range(self._size)] for _ in range(self._size)]

        return tuple(tuple(row) for row in self._pole)
