import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PixelGlyph")
        self.setMinimumSize(900, 600)

        label = QLabel(
            "PixelGlyph\n\nCreated by Benjamin Wilson\n© 2026 Benjamin Wilson"
        )
        label.setStyleSheet("font-size: 24px;")
        label.setMargin(30)

        self.setCentralWidget(label)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())