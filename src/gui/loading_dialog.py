from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class LoadingDialog(QDialog):
    def __init__(self, parent=None, message="PROCESSING..."):
        super().__init__(parent)
        self.setWindowTitle("IfNoAI - System Processing")
        self.setFixedSize(400, 150)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        # Setup Dark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 15))
        palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        self.setPalette(palette)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Message
        self.msg_label = QLabel(message)
        self.msg_label.setStyleSheet("font-family: 'Consolas'; font-size: 14px; color: #00ff88; font-weight: bold;")
        self.msg_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.msg_label)
        
        # Progress Bar (Indeterminate)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0) # Indeterminate
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 5px;
                background-color: #1a1a20;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #00ff88;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Footer
        footer = QLabel("PLEASE WAIT")
        footer.setStyleSheet("color: #666; font-family: 'Consolas'; font-size: 10px; letter-spacing: 2px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

    def set_message(self, msg):
        self.msg_label.setText(msg)
