from PyQt6.QtWidgets import QApplication
import sys
from gui import AssignmentApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssignmentApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
