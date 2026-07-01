from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QStackedWidget
)
from PySide6.QtGui import (
    QPixmap,
    QFont
)
from ascii_converter import image_to_ascii

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PixelGlyph")
        self.setMinimumSize(1000, 700)

        self.selected_image_path = None

        self._create_menu_bar()
        self._create_status_bar()
        self._create_ui()

    def _create_menu_bar(self):
        file_menu = self.menuBar().addMenu("File")
        help_menu = self.menuBar().addMenu("Help")
    
    def _create_status_bar(self):
        self.statusBar().showMessage("Ready")
    
    def _create_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)

        splitter = QSplitter()

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        title_label = QLabel("INPUT")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.select_button = QPushButton("Select Image")

        width_label = QLabel("ASCII Width")
        self.width_input = QLineEdit("120")

        charset_label = QLabel("Character Set")
        self.charset_dropdown = QComboBox()
        self.charset_dropdown.addItems([
            "@%#*+=-:. ",
            "█▓▒░ ",
            "@#$&?!;:. "
        ])

        self.convert_button = QPushButton("Convert")

        left_layout.addWidget(title_label)
        left_layout.addSpacing(20)
        left_layout.addWidget(self.select_button)
        left_layout.addSpacing(20)
        left_layout.addWidget(width_label)
        left_layout.addWidget(self.width_input)
        left_layout.addSpacing(10)
        left_layout.addWidget(charset_label)
        left_layout.addWidget(self.charset_dropdown)
        left_layout.addStretch()
        left_layout.addWidget(self.convert_button)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        preview_label = QLabel("PREVIEW")
        preview_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Image preview
        self.image_preview = QLabel("No image selected.")
        self.image_preview.setMinimumSize(600, 500)
        self.image_preview.setScaledContents(False)

        image_scroll = QScrollArea()
        image_scroll.setWidgetResizable(True)
        image_scroll.setWidget(self.image_preview)

        # ASCII preview
        self.ascii_preview = QTextEdit()
        self.ascii_preview.setReadOnly(True)
        self.ascii_preview.setFont(QFont("Consolas", 8))

        # Switch between image and ASCII views
        self.preview_stack = QStackedWidget()
        self.preview_stack.addWidget(image_scroll)
        self.preview_stack.addWidget(self.ascii_preview)

        right_layout.addWidget(preview_label)
        right_layout.addWidget(self.preview_stack)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        splitter.setSizes([250, 750])

        layout.addWidget(splitter)

        self.select_button.clicked.connect(self.select_image)

        self.convert_button.clicked.connect(self.convert_image)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )

        if file_path:
            self.selected_image_path = file_path
            self.statusBar().showMessage(f"Selected image: {file_path}")
            self.show_image_preview(file_path)
    
    def show_image_preview(self, file_path):
        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            self.statusBar().showMessage("Unable to load image preview.")
            return
        
        scaled_pixmap = pixmap.scaledToWidth(700)

        self.image_preview.setPixmap(scaled_pixmap)
        self.preview_stack.setCurrentIndex(0)

    def convert_image(self):
        if not self.selected_image_path:
            self.statusBar().showMessage("No image selected.")
            return

        try:
            width = int(self.width_input.text())
            charset = self.charset_dropdown.currentText()

            ascii_text = image_to_ascii(
                self.selected_image_path,
                width,
                charset
            )

            self.ascii_preview.setPlainText(ascii_text)
            self.preview_stack.setCurrentIndex(1)

            self.statusBar().showMessage("Conversion complete!")
        
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}")