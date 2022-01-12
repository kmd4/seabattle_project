import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from function_ship import System


class Edit(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('statements\pole_user.ui', self)
        self.s = list(map(lambda x: x, self.channelButtons.buttons()))
        for button in self.s:
            button.clicked.connect(self.step)
        self.a, self.a1 = System().make_new_pole()
        self.setWindowTitle('Морской бой')
        self.setFixedSize(824, 557)
        self.flag = 1
        self.pushButton_102.clicked.connect(self.generation_random)
        self.pushButton_100.clicked.connect(self.clear)
        self.first_cord = ''
        self.where_i_can_go = []
        self.pushButton_101.setEnabled(False)
        self.ships = [4] * 1 + [3] * 2 + [2] * 3 + [1] * 4
        self.list_ships = []

    def step(self):
        index1 = self.s.index(self.sender())
        if self.a1[index1] != 'X' and self.a1[index1] != 'N' and self.flag == 1 and len(set(self.ships)) == 1 and\
                1 in self.ships:
            ship = [str(index1).rjust(2, '0')] + ['horiz']
            System().around_ship(ship, self.a, self.a1)
            self.list_ships.append(ship)
            self.s[index1].setStyleSheet('background: rgb(255, 218, 185);')
            self.ships.remove(1)
        elif self.a1[index1] != 'X' and self.a1[index1] != 'N' and self.flag == 1:
            res = []
            for el in list(set(self.ships)):
                w = list(map(lambda x: x[:-1], System().can_i_make_ship_here(index1, el, self.a1)))
                for el1 in w:
                    res += [el1]
            for i in range(len(res)):
                if len(res[i]) != 1:
                    r = [res[i][0]] + [res[i][-1]]
                    r.remove(str(index1).rjust(2, '0'))
                    res[i] = r
                res[i] = res[i][0]
            self.where_i_can_go = res
            if 1 not in self.ships and str(index1).rjust(2, '0') in self.where_i_can_go:
                self.where_i_can_go.remove(str(index1).rjust(2, '0'))
            if not(self.where_i_can_go == [] and len(self.ships) != 0):
                for el in res:
                    if int(el) // 10 == index1 // 10:
                        self.s[int(el)].setText(str((abs(int(el) - index1) + 1)))
                    else:
                        self.s[int(el)].setText((str(abs((int(el) // 10) - (index1 // 10)) + 1)))
                self.s[index1].setStyleSheet('background: rgb(255, 218, 185);')
                self.first_cord = index1
                self.flag = 2
        elif self.a1[index1] != 'X' and self.a1[index1] != 'N' and self.flag == 2 and str(index1).rjust(2, '0') in\
                self.where_i_can_go:
            my_len = 0
            if self.a1[index1] // 10 == self.first_cord // 10:
                rangeration = sorted([self.a1[index1], self.first_cord])
                rangeration[1] += 1
                ship = list(map(lambda x: str(x).rjust(2, '0'), range(*rangeration))) + ['horiz']
                System().around_ship(ship, self.a, self.a1)
                self.list_ships.append(ship)
                for i in range(*rangeration):
                    self.s[i].setStyleSheet('background: rgb(255, 218, 185);')
                    my_len += 1
            elif self.a1[index1] % 10 == self.first_cord % 10:
                rangeration = sorted([self.a1[index1] // 10, self.first_cord // 10])
                rangeration[1] += 1
                ship = list(map(lambda x: str((10 * x) + (index1 % 10)).rjust(2, '0'), range(*rangeration))) + ['vert']
                System().around_ship(ship, self.a, self.a1)
                for i in range(*rangeration):
                    self.s[(10 * i) + (index1 % 10)].setStyleSheet('background: rgb(255, 218, 185);')
                    my_len += 1
                self.list_ships.append(ship)
            for el in self.where_i_can_go:
                self.s[int(el)].setText('')
            self.ships.remove(my_len)
            self.flag = 1
            self.where_i_can_go = []
        if len(self.ships) == 0:
            self.flag = 0
            self.pushButton_101.setStyleSheet('background: rgb(0, 0, 255); color: rgb(255, 255, 255);')
            self.pushButton_101.setEnabled(True)
        self.label_2.setText(f'Осталось кораблей: {len(self.ships)}')

    def clear(self):
        for button in self.s:
            button.setStyleSheet(None)
            button.setText('')
        self.a, self.a1 = System().make_new_pole()
        self.flag = 1
        self.first_cord = ''
        self.where_i_can_go = []
        self.ships = [4] * 1 + [3] * 2 + [2] * 3 + [1] * 4
        self.list_ships = []
        self.label_2.setText('Осталось кораблей: 10')
        self.pushButton_101.setStyleSheet(None)
        self.pushButton_101.setEnabled(False)

    def generation_random(self):
        self.clear()
        self.a1, self.list_ships = System().make_pole_for_system()
        for i in range(100):
            if self.a1[i] == 'X':
                self.s[i].setStyleSheet('background: rgb(255, 218, 185);')
        self.pushButton_101.setEnabled(True)
        self.pushButton_101.setStyleSheet('background: rgb(0, 0, 255); color: rgb(255, 255, 255);')
        self.label_2.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Edit()
    ex.show()
    sys.exit(app.exec_())