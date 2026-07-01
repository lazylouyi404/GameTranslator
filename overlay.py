import sys
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush

class ModernWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.is_moving = False; self.is_resizing = False; self.old_pos = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()
        local_pos = event.position()
        if local_pos.x() > self.width() - 30 and local_pos.y() > self.height() - 30:
            self.is_resizing = True
        else:
            self.is_moving = True

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_pos
        if self.is_moving: 
            self.move(self.x() + delta.x(), self.y() + delta.y())
        elif self.is_resizing:
            self.resize(max(80, self.width() + delta.x()), max(50, self.height() + delta.y()))
        self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.is_moving = False; self.is_resizing = False

class OCRSelector(ModernWidget):
    def __init__(self, color_type="green"):
        super().__init__()
        self.color_type = color_type
        self.color = QColor(0, 255, 0) if color_type == "green" else QColor(0, 150, 255)
        self.setGeometry(50, 150, 320, 200)

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QBrush(QColor(self.color.red(), self.color.green(), self.color.blue(), 20)))
        p.setPen(QPen(self.color, 3, Qt.PenStyle.SolidLine))
        p.drawRoundedRect(2, 2, self.width()-4, self.height()-4, 10, 10)

    def get_ocr_region(self): 
        return (self.x(), self.y(), self.width(), self.height())
        
    def toggle_visibility(self):
        self.setVisible(not self.isVisible())

class TranslationDisplay(ModernWidget):
    text_received = pyqtSignal(str)
    def __init__(self, color_style="default"):
        super().__init__()
        self.setGeometry(500, 100, 450, 150)
        self.label = QLabel("", self)
        
        # Pengaturan warna berdasarkan mode
        if color_style == "blue":
            self.bg_style = "rgba(0, 40, 80, 100)"  # Biru Transparan untuk Dialog
            self.border = "1px solid rgba(100, 200, 255, 100)"
        else:
            self.bg_style = "rgba(0, 0, 0, 100)"    # Hitam Transparan untuk Misi
            self.border = "1px solid rgba(255, 255, 255, 50)"

        self.label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: white; background-color: transparent;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.text_received.connect(self.update_text)

    def update_text(self, text):
        if not text or text.strip() == "":
            self.label.setText("")
            self.label.setStyleSheet("background-color: transparent; border: none;")
        else:
            self.label.setText(text)
            self.label.setStyleSheet(f"color: white; background-color: {self.bg_style}; border-radius: 10px; padding: 10px; border: {self.border};")

class ScreenToggleButton(QWidget):
    def __init__(self, click_callback):
        super().__init__()
        self.click_callback = click_callback
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setGeometry(10, 150, 55, 55)
        
        self.btn = QPushButton("OCR", self)
        self.btn.setGeometry(2, 2, 50, 50)
        self.btn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff4b2b, stop:1 #ff416c); color: white; border-radius: 25px; font-weight: bold; border: 2px solid white;")
        self.btn.clicked.connect(self.click_callback)
        
        self.is_moving = False; self.old_pos = None

    def mousePressEvent(self, event):
        self.is_moving = True
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.is_moving:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.is_moving = False