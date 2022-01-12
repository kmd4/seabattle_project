from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QDialog


class Input_Name(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('statements\editname.ui', self)
        self.setWindowTitle('Морской бой')
        self.setFixedSize(400, 300)
        self.label_2.setStyleSheet('color: rgb(240, 0, 0);')
        self.label_2.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Input_Name()
    ex.show()
    sys.exit(app.exec_())