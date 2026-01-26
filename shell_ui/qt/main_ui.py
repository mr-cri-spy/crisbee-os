import sys
import os
from PyQt6.QtCore import Qt


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)



from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)

# IMPORTANT: adjust path if needed later
from ai_core.api import process_request

class CrisbeeShell(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(" Crisbee OS v0.5")

        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f14;
                color: #e6e6e6;
                font-family: Inter, Arial;
                font-size: 14px;
            }
            QLabel {
                color: #9effff;
                font-size: 16px;
                font-weight: bold;
            }
            QTextEdit {
                background-color: #0f1720;
                color: #b8fefb;
                border: 1px solid #1f2933;
                border-radius: 8px;
                padding: 8px;
            }
            QLineEdit {
                background-color: #020617;
                color: #ffffff;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Crisbee OS v0.5 Secure AI System Control")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Crisbee...")

        self.button = QPushButton("Send")
        self.button.clicked.connect(self.ask_crisbee)

        layout.addWidget(self.label)
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def ask_crisbee(self):
        user_input = self.input.text().strip()
        if not user_input:
            return

        self.output.append(f"You: {user_input}")

        response = process_request(user_input)

        self.output.append(f"Crisbee: {response['result']}\n")
        self.input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CrisbeeShell()
    window.show()
    sys.exit(app.exec())

