import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)

MODEL = "qwen2.5:7b-instruct"

class CrisbeeShell(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("  Crisbee OS v0.3")
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
        user_input = self.input.text()
        if not user_input:
            return

        self.output.append(f"You: {user_input}")

        result = subprocess.run(
            ["ollama", "run", MODEL],
            input=user_input,
            text=True,
            capture_output=True
        )

        self.output.append(f"Crisbee: {result.stdout.strip()}\n")
        self.input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CrisbeeShell()
    window.show()
    sys.exit(app.exec())
