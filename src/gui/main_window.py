import sys
import ctypes
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QComboBox, QFrame, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QColor, QPalette

# Add src to path to import core
sys.path.append(str(Path(__file__).parents[1]))
from core.blocker import AIBlocker
from core.sinkhole import SinkholeServer
from gui.report_window import ReportWindow
from gui.loading_dialog import LoadingDialog

class WorkerThread(QThread):
    finished = Signal()
    
    def __init__(self, func):
        super().__init__()
        self.func = func
        
    def run(self):
        try:
            self.func()
        except:
            pass
        self.finished.emit()

class ModernButton(QPushButton):
    def __init__(self, text, parent=None, is_danger=False):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(50)
        
        color = "#ff4444" if is_danger else "#00ff88"
        hover_color = "#ff6666" if is_danger else "#33ffaa"
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {color};
                border-radius: 5px;
                color: {color};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 2px;
            }}
            QPushButton:hover {{
                background-color: {color}22;
                border-color: {hover_color};
                color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {color}44;
            }}
            QPushButton:disabled {{
                border-color: #444;
                color: #444;
            }}
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.blocker = AIBlocker()
        self.sinkhole = SinkholeServer()
        self.timer_count = 0
        self.experiment_start_time = None  # Track when experiment started
        self.original_timer_count = 0  # Track original duration for settlement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
        # Stats update timer
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000) # Update stats every second

        self.apply_global_styles()
        self.init_ui()
        self.update_status_display()
        
        # If already blocked on startup, start sinkhole
        if self.blocker.status():
             self.sinkhole.start()

    def apply_global_styles(self):
        style = """
            /* Global Dark Theme */
            QMessageBox {
                background-color: #101015;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-family: 'Consolas';
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: transparent;
                border: 2px solid #00ff88;
                border-radius: 5px;
                color: #00ff88;
                font-family: 'Consolas';
                font-weight: bold;
                padding: 6px 20px;
            }
            QMessageBox QPushButton:hover {
                background-color: #00ff8822;
                color: #33ffaa;
            }
            QMessageBox QPushButton:pressed {
                background-color: #00ff8844;
            }
            
            /* ComboBox Styling */
            QComboBox {
                background-color: #1a1a20;
                border: 1px solid #333;
                padding: 10px;
                color: #ccc;
                font-family: 'Consolas';
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid #00ff88;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #00ff88;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1a20;
                border: 1px solid #333;
                color: #ccc;
                selection-background-color: #00ff88;
                selection-color: #000;
                outline: none;
            }
        """
        if QApplication.instance():
            QApplication.instance().setStyleSheet(style)

    def init_ui(self):
        self.setWindowTitle("IfNoAI - Protocol Console")
        self.setFixedSize(500, 650)
        
        # Setup Dark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 15))
        palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        self.setPalette(palette)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        title = QLabel("IfNoAI")
        title.setStyleSheet("font-family: 'Impact'; font-size: 48px; color: #00ff88; letter-spacing: 4px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("HUMAN INTELLIGENCE ONLY")
        subtitle.setStyleSheet("font-family: 'Consolas'; font-size: 12px; color: #666; letter-spacing: 3px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Status Indicator
        self.status_frame = QFrame()
        self.status_frame.setFixedSize(440, 80)
        status_layout = QVBoxLayout(self.status_frame)
        
        self.status_label = QLabel("SYSTEM SCANNING...")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(self.status_frame, 0, Qt.AlignCenter)

        # Stats Display
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet("background-color: #15151a; border-radius: 5px; border: 1px solid #333;")
        stats_layout = QVBoxLayout(self.stats_frame)
        
        stats_label_title = QLabel("INTERCEPTION LOG")
        stats_label_title.setStyleSheet("color: #888; font-family: 'Consolas'; font-size: 10px; letter-spacing: 1px;")
        stats_layout.addWidget(stats_label_title)
        
        self.stats_count_label = QLabel("0")
        self.stats_count_label.setStyleSheet("color: #00ff88; font-family: 'Consolas'; font-size: 36px; font-weight: bold;")
        self.stats_count_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(self.stats_count_label)

        self.stats_detail_label = QLabel("BLOCKED ATTEMPTS")
        self.stats_detail_label.setStyleSheet("color: #666; font-family: 'Consolas'; font-size: 10px;")
        self.stats_detail_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(self.stats_detail_label)

        layout.addWidget(self.stats_frame)

        # Timer Selection
        self.time_selector = QComboBox()
        self.time_selector.addItems([
            "24 Hours Blackout",
            "8 Hours Workday",
            "4 Hours Focus",
            "1 Hour Test"
        ])
        # Stylesheet is now applied globally
        layout.addWidget(self.time_selector)

        # Countdown Display
        self.timer_display = QLabel("00:00:00")
        self.timer_display.setStyleSheet("font-family: 'Consolas'; font-size: 48px; color: #444;")
        self.timer_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_display)

        # Controls
        self.toggle_btn = ModernButton("INITIATE PROTOCOL")
        self.toggle_btn.clicked.connect(self.toggle_block)
        layout.addWidget(self.toggle_btn)

        layout.addStretch()
        
        footer = QLabel("v1.1.0 // PHASE 3: SINKHOLE ACTIVE")
        footer.setStyleSheet("color: #333; font-family: 'Consolas'; font-size: 10px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

    def update_status_display(self):
        is_active = self.blocker.status()
        self.toggle_btn.setEnabled(True) # Always re-enable button when status updates
        
        if is_active:
            self.status_label.setText("CONNECTION SEVERED")
            self.status_label.setStyleSheet("color: #ff4444; font-family: 'Consolas'; font-size: 24px; font-weight: bold;")
            self.status_frame.setStyleSheet("background-color: #1a0f0f; border: 1px solid #ff4444; border-radius: 10px;")
            self.toggle_btn.setText("ABORT PROTOCOL")
            self.toggle_btn.setStyleSheet(self.toggle_btn.styleSheet().replace("#00ff88", "#ff4444").replace("#33ffaa", "#ff6666"))
            self.time_selector.setEnabled(False)
            self.stats_count_label.setStyleSheet("color: #ff4444; font-family: 'Consolas'; font-size: 36px; font-weight: bold;")
        else:
            self.status_label.setText("ONLINE")
            self.status_label.setStyleSheet("color: #00ff88; font-family: 'Consolas'; font-size: 24px; font-weight: bold;")
            self.status_frame.setStyleSheet("background-color: #0f1a15; border: 1px solid #00ff88; border-radius: 10px;")
            self.toggle_btn.setText("INITIATE PROTOCOL")
            # Simple reset of button style
            self.toggle_btn.setStyleSheet(self.toggle_btn.styleSheet().replace("#ff4444", "#00ff88").replace("#ff6666", "#33ffaa"))
            self.time_selector.setEnabled(True)
            self.stats_count_label.setStyleSheet("color: #00ff88; font-family: 'Consolas'; font-size: 36px; font-weight: bold;")

    def toggle_block(self):
        if not self.blocker.is_admin():
            QMessageBox.warning(self, "Permission Denied", "Please run IfNoAI as Administrator.")
            return

        self.toggle_btn.setEnabled(False) # Prevent double clicks

        if self.blocker.status():
            # Currently Active -> Deactivate
            reply = QMessageBox.question(self, "Confirm Abort", 
                                       "Are you sure you want to reconnect to the AI cloud?\nThe experiment is not finished.",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.timer.stop()
                
                # Show loading dialog
                self.loading_dialog = LoadingDialog(self, "RECONNECTING TO NEURAL NET...")
                self.loading_dialog.setModal(True)
                self.loading_dialog.show()
                
                # Run disable in background
                def stop_tasks():
                    self.blocker.disable_block()
                    self.sinkhole.stop()
                
                self.worker = WorkerThread(stop_tasks)
                self.worker.finished.connect(self.on_stop_finished)
                self.worker.start()
            else:
                self.toggle_btn.setEnabled(True) # Re-enable if cancelled
                
        else:
            # Currently Inactive -> Activate
            duration_idx = self.time_selector.currentIndex()
            hours = [24, 8, 4, 1][duration_idx]
            
            # Show loading dialog for start too (can take a moment)
            self.loading_dialog = LoadingDialog(self, "SEVERING NEURAL LINKS...")
            self.loading_dialog.setModal(True)
            self.loading_dialog.show()
            
            def start_tasks():
                return self.blocker.enable_block()

            # Create a custom worker that can return value
            self.worker = WorkerThread(lambda: None) # Placeholder
            self.worker.run = lambda: setattr(self.worker, 'result', start_tasks())
            self.worker.finished.connect(lambda: self.on_start_finished(getattr(self.worker, 'result', False), hours))
            self.worker.start()

    def on_stop_finished(self):
        self.loading_dialog.close()
        # Check if report is already open or we are already done
        if not hasattr(self, '_report_shown') or not self._report_shown:
            self._report_shown = True
            self.finish_experiment()
            self._report_shown = False # Reset after close
        
        self.timer_display.setText("00:00:00")
        self.timer_display.setStyleSheet("font-family: 'Consolas'; font-size: 48px; color: #444;")
        self.update_status_display()

    def on_start_finished(self, success, hours):
        self.loading_dialog.close()
        if success:
            self._report_shown = False # Reset flag on start
            self.sinkhole.start()
            self.start_timer(hours * 3600)
            self.update_status_display()

    def start_timer(self, seconds):
        self.timer_count = seconds
        self.original_timer_count = seconds  # Store original duration
        self.experiment_start_time = datetime.now()  # Record start time
        self.update_timer_display()
        self.timer_display.setStyleSheet("font-family: 'Consolas'; font-size: 48px; color: #ff4444;")
        self.timer.start(1000)

    def update_timer(self):
        self.timer_count -= 1
        self.update_timer_display()
        
        if self.timer_count <= 0:
            self.timer.stop()
            self.toggle_btn.setEnabled(False) # Disable button during auto-stop
            # Async finish for timer expiry
            self.loading_dialog = LoadingDialog(self, "PROTOCOL COMPLETE. DISENGAGING...")
            self.loading_dialog.setModal(True)
            self.loading_dialog.show()
            
            def stop_tasks():
                self.blocker.disable_block()
                self.sinkhole.stop()
            
            self.worker = WorkerThread(stop_tasks)
            self.worker.finished.connect(self.on_stop_finished)
            self.worker.start()

    def finish_experiment(self):
        # This method is now called AFTER blocking is disabled by worker (if manually stopped)
        # OR called by timer (needs to disable blocking)
        
        # If called by timer, we need to disable blocking synchronously or async?
        # For simplicity, if timer calls it, we might freeze briefly, or we should use async there too.
        # But finish_experiment is also called by on_stop_finished where blocking is ALREADY disabled.
        
        # Let's check if blocking is still active.
        if self.blocker.status():
             self.blocker.disable_block()
             self.sinkhole.stop()
        
        self.update_status_display()
        
        # Prepare Stats
        stats = self.sinkhole.get_stats()
        count = stats['total_blocked']
        
        # Calculate actual duration
        if self.experiment_start_time:
            duration = datetime.now() - self.experiment_start_time
            # Format duration nicely
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            parts = []
            if hours > 0:
                parts.append(f"{hours}h")
            if minutes > 0:
                parts.append(f"{minutes}m")
            parts.append(f"{seconds}s")
            duration_str = " ".join(parts)
        else:
            # Fallback if something went wrong with start time
            duration_idx = self.time_selector.currentIndex()
            duration_str = ["24 Hours", "8 Hours", "4 Hours", "1 Hour"][duration_idx]
        
        # Show Report Window
        report = ReportWindow(duration_str, count, stats['domains'], self)
        report.exec()

    def update_timer_display(self):
        h = self.timer_count // 3600
        m = (self.timer_count % 3600) // 60
        s = self.timer_count % 60
        self.timer_display.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def update_stats(self):
        if self.blocker.status():
            stats = self.sinkhole.get_stats()
            total = stats['total_blocked']
            self.stats_count_label.setText(str(total))
            
            # Optional: Show top domain in detail label if active
            if total > 0:
                top_domain = max(stats['domains'], key=stats['domains'].get)
                self.stats_detail_label.setText(f"LATEST: {top_domain}")

    def closeEvent(self, event):
        self.sinkhole.stop()
        super().closeEvent(event)

def run_as_admin():
    """Relaunch the current script as administrator."""
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    
    # Re-run the program with admin rights
    try:
        if sys.argv[0].endswith('.exe'):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.argv[0], " ".join(sys.argv[1:]), None, 1)
        else:
            # Need to quote the script path in case of spaces
            script = sys.argv[0]
            params = " ".join([f'"{arg}"' if " " in arg else arg for arg in sys.argv[1:]])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        return False # The new process started, so we exit this one
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")
        return False

if __name__ == "__main__":
    if not run_as_admin():
        sys.exit(0)
        
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
