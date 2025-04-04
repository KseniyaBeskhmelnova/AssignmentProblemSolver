from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout
import numpy as np

class MatrixInputDialog(QDialog):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.setWindowTitle("Manual Matrix Input")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Matrix C:"))
        grid_layout = QGridLayout()
        self.c_inputs = [[QLineEdit() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                grid_layout.addWidget(self.c_inputs[i][j], i, j)
        layout.addLayout(grid_layout)

        layout.addWidget(QLabel("Vector X:"))
        x_layout = QHBoxLayout()
        self.x_inputs = [QLineEdit() for _ in range(n)]
        for i in range(n):
            x_layout.addWidget(self.x_inputs[i])
        layout.addLayout(x_layout)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_values(self):
        C = np.zeros((self.n, self.n))
        X = np.zeros(self.n)
        try:
            for i in range(self.n):
                for j in range(self.n):
                    C[i, j] = float(self.c_inputs[i][j].text())
                X[i] = float(self.x_inputs[i].text())
            return C, X
        except ValueError:
            return None, None
