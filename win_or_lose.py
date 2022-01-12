from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
import sqlite3


class Win(QDialog):
    def __init__(self):
        super().__init__()
        f = open('statements\win_or_lose.txt', encoding='utf-8').read()
        self.state, self.name = f.split('\n')
        uic.loadUi('statements\win_or_lose.ui', self)
        self.setWindowTitle('Морской бой')
        self.setFixedSize(450, 300)
        self.label.setText(self.state)
        con = sqlite3.connect("statements\data_base.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT wins, games  FROM base
                    WHERE name = ?""", (self.name,)).fetchall()
        con.close()
        self.label_2.setText(f'Всего игр: {result[0][1]}, из них побед: {result[0][0]}')
        self.pushButton.clicked.connect(self.push2)

    def push2(self):
        w = QMessageBox()
        valid = w.question(
            self, 'Морской бой', "Сбросить прогресс?",
            w.Yes, w.No)
        if valid == w.Yes:
            con = sqlite3.connect("statements\data_base.sqlite")
            cur = con.cursor()
            cur.execute(f"""UPDATE base
                SET games = 0, wins = 0 
                WHERE name = ?""", (self.name,))
            con.commit()
            con.close()
            self.label_2.setText('Всего игр: 0, из них побед: 0')
            self.pushButton.setEnabled(False)
        else:
            w.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Win()
    ex.show()
    sys.exit(app.exec_())