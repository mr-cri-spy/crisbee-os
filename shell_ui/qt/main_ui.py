import sys
import os

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

        self.setWindowTitle(" Crisbee OS v0.4")
        self.setGeometry(300, 200, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Crisbee AI Shell")
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

