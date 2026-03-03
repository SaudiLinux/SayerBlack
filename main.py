import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal
from engine.scanner import run_full_scan
from db.database import save_scan

class ScanThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self, target):
        super().__init__()
        self.target = target

    def run(self):
        def log_callback(level, message):
            pass  # Simple log callback for now
        results = run_full_scan(self.target, self.progress.emit, log_callback)
        self.finished.emit(results)

class SayerBlack(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SayerBlack Pro - SayerLinux")
        self.setGeometry(200, 200, 1100, 700)

        self.setStyleSheet("""
            QMainWindow { background-color: #0d0d0d; }
            QLabel { color: #00ff99; font-size: 14px; }
            QTextEdit { background-color: #1a1a1a; color: #00ff00; }
            QPushButton { background-color: #111; color: #00ff99; padding: 6px; }
            QProgressBar { background-color: #111; color: #00ff99; }
        """)

        self.init_ui()

    def init_ui(self):

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter Target URL or IP")

        self.ctf_checkbox = QCheckBox("Enable CTF Mode")

        self.start_button = QPushButton("Start Scan")
        self.start_button.clicked.connect(self.start_scan)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.tabs = QTabWidget()
        self.results_tab = QTextEdit()
        self.network_tab = QTextEdit()
        self.tabs.addTab(self.results_tab, "Vulnerabilities")
        self.tabs.addTab(self.network_tab, "Network")

        self.console_tab = QTextEdit()
        self.console_tab.setReadOnly(True)
        self.tabs.addTab(self.console_tab, "Live Console")
        
        self.exploit_tab = QWidget() 
        self.tabs.addTab(self.exploit_tab, "Exploit Lab") 
        self.init_exploit_tab()

        layout.addWidget(QLabel("SayerBlack Pro - Developer: SayerLinux"))
        layout.addWidget(self.target_input)
        layout.addWidget(self.ctf_checkbox)
        layout.addWidget(self.start_button)
        layout.addWidget(self.progress)
        layout.addWidget(self.tabs)

        central.setLayout(layout)

    def init_exploit_tab(self):
        pass

    def start_scan(self):
        target = self.target_input.text()
        self.thread = ScanThread(target)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(self.display_results)
        self.thread.start()

    def display_results(self, results):
        self.results_tab.setText(str(results.get("vulns", "")))
        self.network_tab.setText(str(results.get("network", "")))
        save_scan(self.target_input.text(), results)
        self.progress.setValue(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SayerBlack()
    window.show()
    sys.exit(app.exec())