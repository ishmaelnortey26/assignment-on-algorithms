import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from GUI.UI.main_window import MainUI


def main():
    # Enable HiDPI scaling (important on macOS / Retina)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    window = MainUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
