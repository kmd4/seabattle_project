from PyQt5 import uic
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow


class First(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('statements\First.ui', self)
        self.pushButton.setStyleSheet('background: rgb(255, 255, 255);')
        self.pushButton_2.setStyleSheet('background: rgb(255, 255, 255);')
        self.pushButton.clicked.connect(self.push)
        self.setWindowTitle('Морской бой')
        self.setFixedSize(1200, 671)
        self.load_mp3()

    def load_mp3(self):
        self.playlist = QMediaPlaylist()
        url = QUrl.fromLocalFile("statements\music1.mp3")
        self.playlist.addMedia(QMediaContent(url))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.play()

    def push(self):
        return 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = First()
    ex.show()
    sys.exit(app.exec_())