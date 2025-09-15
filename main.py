import sys
import logging
from PyQt5.QtWidgets import QApplication
from ui_mainwindow import MainWindow

logging.basicConfig(level=logging.INFO)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
