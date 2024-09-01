import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import QTimer, Qt, QSize
import psutil

class CPUMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)

    def sizeHint(self):
        return QSize(50, 150)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()

        cpu_percent = psutil.cpu_percent()

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(0, 0, w-1, h-1)

        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(3, 10, "CPU {0:.0f}%".format(cpu_percent))

        qp.setPen(QColor(34, 139, 34))
        qp.setBrush(QColor(34, 139, 34))
        qp.drawRect(10, 15, cpu_percent, h-25)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.wid = CPUMonitor()
        self.setCentralWidget(self.wid)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('CPU Monitor')
        self.show()

    def update(self):
        self.wid.repaint()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
