import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5 import uic, QtCore
import random
from function_ship import System
from first import First
from input_name import Input_Name
from edit import Edit
from win_or_lose import Win


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('statements\game.ui', self)
        self.first_window = First()
        self.first_window.show()
        self.first_window.pushButton_2.hide()
        self.first_window.pushButton.clicked.connect(self.push_change_name)
        self.pushButton_301.clicked.connect(self.break_game)
        self.s1 = list(map(lambda x: x, self.firstButtons.buttons()))
        for button in self.s1:
            button.clicked.connect(self.system)
        self.s2 = list(map(lambda x: x, self.secondButtons.buttons()))
        self.setWindowTitle('Морской бой')
        self.setFixedSize(1100, 663)
        self.flag_it_win = 0

    def show_input_window(self):
        self.first_window.hide()
        self.input_window = Input_Name()
        self.input_window.show()
        self.input_window.pushButton.clicked.connect(self.get_name)

    def get_name(self):
        if self.input_window.lineEdit.text() == '':
            self.input_window.label_2.show()
        else:
            self.name = self.input_window.lineEdit.text()
            self.show_edit_window()

    def push_new_game(self):
        self.first_window.hide()
        self.flag_change_name = 0
        self.show_edit_window()

    def push_change_name(self):
        self.first_window.hide()
        self.flag_change_name = 1
        self.show_input_window()

    def show_edit_window(self):
        if self.flag_change_name == 0:
            self.first_window.hide()
        else:
            self.input_window.close()
        self.edit_window = Edit()
        self.edit_window.show()
        self.edit_window.pushButton_101.clicked.connect(self.show_game_window)

    def show_game_window(self):
        self.first_window.player.stop()
        pole = System().make_pole_for_system()
        for i in range(100):
            if self.edit_window.a1[i] != 'X':
                self.edit_window.a1[i] = 'N'
        self.sys_ships, self.user_ships = [], []  # список кораблей системы 'vert', 'horiz'
        for el in pole[1]:
            self.sys_ships.append(el)
        for el in self.edit_window.list_ships:
            self.user_ships.append(el)
        for button in self.s1:
            button.setStyleSheet(None)
            button.setEnabled(True)
        for button in self.s2:
            button.setStyleSheet(None)
            button.setEnabled(True)
        self.edit_window.close()
        self.label_2.setText(self.name)
        self.pushButton.setText('<')
        self.sys_pole = ''.join(pole[0]) # поле системы 'X', 'N'
        self.user_pole = ''.join(self.edit_window.a1)
        self.pushButton.setEnabled(False)
        self.beated_user, self.beated_system = [], []  # координаты попаданий
        self.pushButton.setStyleSheet('background: rgb(0, 0, 255); color: rgb(255, 255, 255);')
        self.where_system_can_beat = list(map(lambda i: i, range(100)))
        self.hod = 1
        self.flag_we_got_it = None
        for i in range(100):
            if self.user_pole[i] == 'X': self.s2[i].setStyleSheet('background: rgb(255, 255, 255);')
        self.flag_be_slowly = 0
        self.con = sqlite3.connect("statements\data_base.sqlite")
        self.cur = self.con.cursor()
        ex.show()

    def break_game(self):
        if self.flag_it_win == 0:
            w = QMessageBox()
            valid = w.question(
                self, 'Морской бой', "Завершить игру?",
                w.Yes, w.No)
            if valid == w.Yes:
                ex.hide()
                self.first_window = First()
                self.first_window.show()
                self.first_window.pushButton_2.clicked.connect(self.push_change_name)
                self.first_window.pushButton.clicked.connect(self.push_new_game)

            else:
                w.close()
        else:
            self.flag_it_win = 0
            ex.hide()
            self.first_window = First()
            self.first_window.show()
            self.first_window.pushButton_2.clicked.connect(self.push_change_name)
            self.first_window.pushButton.clicked.connect(self.push_new_game)

    def system(self):   #пользователь бьет поле системы
        if self.hod == 1:
            index1 = self.s1.index(self.sender())
            if self.sys_pole[index1] == 'N':
                self.s1[index1].setStyleSheet('background: rgb(197, 208, 230);')
                self.hod = 2
                QTimer.singleShot(600, self.change_hod)
                QTimer.singleShot(1000, self.user)
            else:
                self.s1[index1].setStyleSheet('background: rgb(0, 0, 128);')
                self.beated_system.append(index1)
                self.is_beat(index1, self.sys_ships, self.beated_system, self.s1)
            self.s1[index1].setEnabled(False)

    def is_beat(self, x, list_ships, beat, pole):
        flag, sh = 0, ''
        for el in list_ships:
            if str(x).rjust(2, '0') in el:
                sh = el
                for el1 in el[:-1]:
                    if int(el1) not in beat:
                        flag = 1
                        return False
        if flag == 0:
            s = sorted(list(map(lambda x: int(x), sh[:-1])))
            res = []
            if sh[-1] == 'vert':
                for i in range(3):
                    res.append(System().is_item_in_list(s[0] - (11 - i), range(s[0] - s[0] % 10 - 10, s[0] - s[0] % 10)))
                for i in range(3):
                    if s[-1] // 10 < 9:
                        res.append(System().is_item_in_list(s[-1] + (11 - i), range((s[-1] // 10 + 1) * 10, (s[-1] // 10 + 2) * 10)))
                for i in range(len(s)):
                    res.append(System().is_item_in_list(s[i] - 1, range(s[i] - s[i] % 10, (s[i] // 10 + 1) * 10)))
                    res.append(System().is_item_in_list(s[i] + 1, range(s[i] - s[i] % 10, (s[i] // 10 + 1) * 10)))
            else:
                for i in range(len(s) + 2):
                    res.append(System().is_item_in_list(s[0] - 11 + i, range((s[0] // 10 - 1) * 10, s[0] // 10 * 10)))
                for i in range(len(s) + 2):
                    if s[0] // 10 != 9:
                        res.append(System().is_item_in_list(s[0] + 9 + i, range((s[0] // 10 + 1) * 10, (s[0] // 10 + 2) * 10)))
                res.append(System().is_item_in_list(s[0] - 1, range(s[0] - s[0] % 10, (s[0] // 10 + 1) * 10)))
                res.append(System().is_item_in_list(s[-1] + 1, range(s[0] - s[0] % 10, (s[0] // 10 + 1) * 10)))
            res = filter(lambda x: x >= 0, res)
            for el in res:
                pole[el].setStyleSheet('background: rgb(197, 208, 230);')
                if self.hod == 2 and el in self.where_system_can_beat:
                    self.where_system_can_beat.pop(self.where_system_can_beat.index(el))
                pole[el].setEnabled(False)
            if len(self.beated_user) == 20 or len(self.beated_system) == 20:
                self.flag_it_win = 1
                if len(self.beated_user) == 20: wi = 0
                else: wi = 1
                if (self.name,) not in self.cur.execute("""SELECT name FROM base""").fetchall():
                    self.cur.execute("""INSERT INTO base(name,wins, games) VALUES(?, ?, ?)""", (self.name, 0, 0))
                    self.con.commit()
                self.cur.execute(f"""UPDATE base
                SET games = games + 1, wins = wins + {wi} 
                WHERE name = ?""", (self.name,))
                self.con.commit()
                self.con.close()
                f = open('statements\win_or_lose.txt', 'w', encoding='utf-8')
                if len(self.beated_user) == 20:
                    for i in range(100):
                        if self.sys_pole[i] == 'X' and i not in self.beated_system:
                            self.s1[i].setStyleSheet('background: rgb(230, 0, 0);')
                    f.write('Поражение')
                    f.write('\n')
                    f.write(self.name)
                elif len(self.beated_system) == 20:
                    f.write('Победа')
                    f.write('\n')
                    f.write(self.name)
                f.close()
                self.win = Win()
                self.win.show()
                self.win.pushButton_2.clicked.connect(self.push_ok)
            elif self.hod == 2 and self.flag_we_got_it == None:
                QTimer.singleShot(1000, self.user)
                return True

    def push_ok(self):
        self.win.close()
        self.break_game()

    def user(self):
        if self.hod == 2:
            step = random.choice(self.where_system_can_beat)
            if self.flag_we_got_it == None and self.user_pole[step] == 'X':
                self.where_system_can_beat.pop(self.where_system_can_beat.index(step))
                self.s2[step].setStyleSheet('background: rgb(0, 0, 128);')
                self.beated_user.append(step)
                self.is_beat(step, self.user_ships, self.beated_user, self.s2)
                QtCore.QTimer.singleShot(1000, lambda: self.we_got_it((step,)))
            elif self.flag_we_got_it != None:
                self.we_got_it(self.flag_we_got_it)
            elif self.user_pole[step] == 'N':
                self.it_N(step)

    def we_got_it(self, x):
        if len(x) == 1:
            x = x[0]
            sh = ''
            for el in self.user_ships:
                if str(x).rjust(2, '0') in el[:-1]:
                    sh = el[:-1]
                    break
            if len(sh) != 1:
                self.flag_we_got_it = (x,)
                self.flag_be_slowly = 1
                list_where = []
                if (x + 1) // 10 == x // 10 and x + 1 in self.where_system_can_beat: list_where.append(x + 1)
                if (x - 1) // 10 == x // 10 and x - 1 in self.where_system_can_beat: list_where.append(x - 1)
                if x // 10 != 9 and x + 10 in self.where_system_can_beat: list_where.append(x + 10)
                if x // 10 != 0 and x - 10 in self.where_system_can_beat: list_where.append(x - 10)
                d = random.choice(list_where)
                if self.user_pole[d] == 'N':
                    self.it_N(d)
                else:
                    self.s2[d].setStyleSheet('background: rgb(0, 0, 128);')
                    self.where_system_can_beat.pop(self.where_system_can_beat.index(d))
                    self.beated_user.append(d)
                    if len(sh) == 2:
                        self.flag_we_got_it = None
                        self.is_beat(d, self.user_ships, self.beated_user, self.s2)
                    else:
                        k1, k2 = sorted([x, d])
                        self.flag_we_got_it = (k1, k2, sh, len(sh) - 2)
                        self.we_got_it(self.flag_we_got_it)
        else:
            new = []
            k1, k2 = self.flag_we_got_it[0:2]
            if k1 // 10 == k2 // 10: #horiz
                if (k1 - 1) // 10 == k1 // 10 and (k1 - 1) in self.where_system_can_beat: new.append(k1 - 1)
                if (k2 + 1) // 10 == k2 // 10 and (k2 + 1) in self.where_system_can_beat: new.append(k2 + 1)
            else:
                if k1 // 10 != 0 and k1 - 10 in self.where_system_can_beat: new.append(k1 - 10)
                if k2 // 10 != 9 and k2 + 10 in self.where_system_can_beat: new.append(k2 + 10)
            elem = random.choice(new)
            if self.user_pole[elem] == 'N':
                if self.flag_be_slowly != 0:
                    QtCore.QTimer.singleShot(1000 * self.flag_be_slowly, lambda: self.it_N(elem))
                else:
                    self.it_N(elem)
                self.flag_be_slowly = 0
            else:
                k1, k2 = sorted([k1, k2, elem])[0], sorted([k1, k2, elem])[-1]
                self.where_system_can_beat.pop(self.where_system_can_beat.index(elem))
                if self.flag_be_slowly != 0: QtCore.QTimer.singleShot(1000 * self.flag_be_slowly, lambda: self.paint(elem))
                else:
                    self.paint(elem)
                self.flag_be_slowly += 1
                self.beated_user.append(elem)
                n = self.flag_we_got_it[3]
                if n > 1:
                    self.flag_we_got_it = (k1, k2, self.flag_we_got_it[2], n - 1)
                    self.we_got_it(self.flag_we_got_it)
                else:
                    self.flag_we_got_it = None
                    if self.flag_be_slowly != 0:
                        QtCore.QTimer.singleShot(1000 * (self.flag_be_slowly - 1), lambda: self.is_beat(k1, self.user_ships, self.beated_user, self.s2))
                    else:
                        self.is_beat(k1, self.user_ships, self.beated_user, self.s2)

    def it_N(self, x):
        self.s2[x].setStyleSheet('background: rgb(197, 208, 230);')
        self.where_system_can_beat.pop(self.where_system_can_beat.index(x))
        if self.hod == 1:
            self.hod = 2
        else:
            self.hod = 3
        QTimer.singleShot(600, self.change_hod)

    def change_hod(self):
        if self.hod == 2:
            self.pushButton.setText('>')
        else:
            self.hod = 1
            self.pushButton.setText('<')

    def paint(self, elem):
        self.s2[elem].setStyleSheet('background: rgb(0, 0, 128);')

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.hide()
    sys.excepthook = except_hook
    sys.exit(app.exec_())