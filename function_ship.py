import random


class System():
    def __init__(self):
        self.ships = []

    def make_new_pole(self):  # функция создает два поля. Первое- список списков, второе - список
        a = list(map(lambda i: list(range(i * 10, (i + 1) * 10)), range(10)))
        a1 = list(map(lambda i: i, range(100)))
        return a, a1

    def can_i_make_ship_here(self, f, n, a1):
        res = []
        if f % 10 + n - 1 < 10:
            right = list(map(lambda x: str(a1[x]).rjust(2, '0'), range(f, f + n)))
            if len(set(map(lambda x: x[0], right))) == 1 and '0X' not in right and '0N' not in right:
                right.append('horiz')
                if n != 1:
                    res.append(right)
        if f % 10 - n + 1 >= 0:
            left = list(map(lambda x: str(a1[x]).rjust(2, '0'), range(f - n + 1, f + 1)))
            if len(set(map(lambda x: x[0], left))) == 1 and '0X' not in left and '0N' not in left:
                left.append('horiz')
                res.append(left)
        if f // 10 - n + 1 >= 0 >= 0:
            top = list(map(lambda x: str(a1[x * 10 + f % 10]).rjust(2, '0'), range(f // 10 - n + 1, f // 10 + 1)))
            if list(map(lambda x: x[-2], top)) == list(map(lambda x: str(x), range(f // 10 - n + 1, f // 10 + 1))):
                top.append('vert')
                if n != 1:
                    res.append(top)
        if (f // 10) + n - 1 < 10:
            bottom = list(map(lambda x: str(a1[x * 10 + f % 10]).rjust(2, '0'), range(f // 10, f // 10 + n)))
            if list(map(lambda x: x[-2], bottom)) == list(map(lambda x: str(x), range(f // 10, f // 10 + n))):
                bottom.append('vert')
                if n != 1:
                    res.append(bottom)
        return res

    def is_item_in_list(self, b, a):
        if b in a:
            return b
        return -1

    def around_ship(self, list1, a, a1):  # Закрашивает корабли '!X!' и клетки вокруг корабля 'N', на которые больше нельзя поставить
        s = list(map(lambda x: int(x), list1[:-1]))
        for el in s:
            a1[el], a[el // 10][el % 10] = 'X', 'X'
        res = []
        if list1[-1] == 'vert':
            for i in range(3):
                res.append(self.is_item_in_list(s[0] - (11 - i), a[s[0] // 10 - 1]))
            for i in range(3):
                if s[-1] // 10 < 9:
                    res.append((self.is_item_in_list(s[-1] + (11 - i), a[s[-1] // 10 + 1])))
            for i in range(len(s)):
                res.append(self.is_item_in_list(s[i] - 1, a[s[i] // 10]))
                res.append(self.is_item_in_list(s[i] + 1, a[s[i] // 10]))
        else:
            for i in range(len(s) + 2):
                res.append(self.is_item_in_list(s[0] - 11 + i, a[s[0] // 10 - 1]))
            for i in range(len(s) + 2):
                if s[0] // 10 != 9:
                    res.append(self.is_item_in_list(s[0] + 9 + i, a[s[0] // 10 + 1]))
            res.append(self.is_item_in_list(s[0] - 1, a[s[0] // 10]))
            res.append(self.is_item_in_list(s[-1] + 1, a[s[0] // 10]))
        res = list(filter(lambda x: x >= 0, res))
        for el in res:
            a1[el] = 'N'
            a[el // 10][el % 10] = 'N'
        return res

    def make_ship(self, n, a, a1):  # подается список чисел 1 до 100, n - длина корабля
        while True:
            f = random.choice(a1)
            if str(f).isdigit():
                ship = self.can_i_make_ship_here(f, n, a1)
                if ship != []:
                    one_ship = random.choice(ship)
                    self.around_ship(one_ship, a, a1)
                    self.ships.append(one_ship)
                    break

    def make_pole_for_system(self):
        a, a1 = self.make_new_pole()
        for el in [4] * 1 + [3] * 2 + [2] * 3 + [1] * 4:
            self.make_ship(el, a, a1)
        for i in range(100):
            if a1[i] != 'X':
                a1[i] = 'N'
        return a1, self.ships