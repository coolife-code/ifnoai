from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QFrame, 
                             QScrollArea, QWidget, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class ReportWindow(QDialog):
    def __init__(self, duration_str, total_blocked, top_domains, parent=None):
        super().__init__(parent)
        self.setWindowTitle("IfNoAI - Experiment Report")
        self.setFixedSize(500, 700)
        
        # Setup Dark Theme (matching main window)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 15))
        palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Header
        title = QLabel("PROTOCOL COMPLETE")
        title.setStyleSheet("font-family: 'Impact'; font-size: 36px; color: #00ff88; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Philosophical Question
        quote = QLabel('"If there were no AI, would you still practice your ideas?"')
        quote.setWordWrap(True)
        quote.setStyleSheet("""
            font-family: 'Georgia', serif; 
            font-style: italic;
            font-size: 18px; 
            color: #fff; 
            margin: 20px 0;
        """)
        quote.setAlignment(Qt.AlignCenter)
        layout.addWidget(quote)

        # Stats Container
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            background-color: #15151a; 
            border: 1px solid #333; 
            border-radius: 10px;
        """)
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setSpacing(15)

        # Duration
        self._add_stat_row(stats_layout, "DURATION", duration_str)
        # Total Interceptions
        self._add_stat_row(stats_layout, "TOTAL INTERCEPTIONS", str(total_blocked), value_color="#ff4444")

        layout.addWidget(stats_frame)

        # Top Domains List
        if top_domains:
            domains_label = QLabel("TOP INTERCEPTED TARGETS")
            domains_label.setStyleSheet("color: #666; font-family: 'Consolas'; font-size: 12px; margin-top: 10px;")
            domains_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(domains_label)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("background: transparent; border: none;")
            
            domain_container = QWidget()
            domain_layout = QVBoxLayout(domain_container)
            domain_layout.setSpacing(5)
            
            # Sort domains by count descending
            sorted_domains = sorted(top_domains.items(), key=lambda x: x[1], reverse=True)
            
            for domain, count in sorted_domains[:10]: # Show top 10
                row = QFrame()
                row.setStyleSheet("background-color: #1a1a20; border-radius: 5px;")
                row_layout = QVBoxLayout(row)
                row_layout.setContentsMargins(10, 5, 10, 5)
                
                d_label = QLabel(f"{domain}")
                d_label.setStyleSheet("color: #ccc; font-family: 'Consolas'; font-weight: bold;")
                
                c_label = QLabel(f"{count} attempts")
                c_label.setStyleSheet("color: #666; font-family: 'Consolas'; font-size: 10px;")
                
                row_layout.addWidget(d_label)
                row_layout.addWidget(c_label)
                domain_layout.addWidget(row)

            domain_layout.addStretch()
            scroll.setWidget(domain_container)
            layout.addWidget(scroll)

        # Close Button
        close_btn = QPushButton("CLOSE REPORT")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFixedHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #00ff88;
                border-radius: 5px;
                color: #00ff88;
                font-family: 'Consolas';
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: #00ff8822;
                color: #33ffaa;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _add_stat_row(self, layout, label, value, value_color="#00ff88"):
        container = QFrame()
        l = QVBoxLayout(container)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(2)
        
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #666; font-family: 'Consolas'; font-size: 10px;")
        lbl.setAlignment(Qt.AlignCenter)
        
        val = QLabel(value)
        val.setStyleSheet(f"color: {value_color}; font-family: 'Consolas'; font-size: 24px; font-weight: bold;")
        val.setAlignment(Qt.AlignCenter)
        
        l.addWidget(val)
        l.addWidget(lbl)
        layout.addWidget(container)
