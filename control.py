from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self, ocr_pairs):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background: rgba(45, 45, 45, 230); border-radius: 10px; color: white;")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>CONTROL PANEL</b>", alignment=Qt.AlignmentFlag.AlignCenter))
        for i, pair in enumerate(ocr_pairs):
            btn = QPushButton(f"Toggle OCR {i+1}")
            btn.setStyleSheet("background: #444; border-radius: 5px; padding: 8px;")
            btn.clicked.connect(lambda _, s=pair['selector'], d=pair['display']: [s.hide(), d.hide()] if s.isVisible() else [s.show(), d.show()])
            layout.addWidget(btn)
        self.setLayout(layout); self.move(10, 10)