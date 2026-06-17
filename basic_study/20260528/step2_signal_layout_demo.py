import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt, Signal


class CounterWidget(QWidget):

    value_changed = Signal(int, int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Step2: Signal & Layout Demo")
        self.resize(400, 250)

        self._count = 0

        self._count_label = QLabel("0")
        self._count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._count_label.setStyleSheet("font-size: 48px; font-weight: bold;")

        self._btn_inc = QPushButton("+")
        self._btn_dec = QPushButton("-")
        self._btn_reset = QPushButton("Reset")

        self._step_label = QLabel("Step:")
        self._step_spin = QSpinBox()
        self._step_spin.setRange(1, 100)
        self._step_spin.setValue(1)

        self._status_label = QLabel("Ready")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("color: gray;")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self._btn_dec)
        btn_layout.addWidget(self._btn_reset)
        btn_layout.addWidget(self._btn_inc)

        step_layout = QHBoxLayout()
        step_layout.addWidget(self._step_label)
        step_layout.addWidget(self._step_spin)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._count_label)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(step_layout)
        main_layout.addWidget(self._status_label)
        self.setLayout(main_layout)

        self._btn_inc.clicked.connect(self._increment)
        self._btn_dec.clicked.connect(self._decrement)
        self._btn_reset.clicked.connect(self._reset)
        self.value_changed.connect(self._update_status)

    def _increment(self):
        old = self._count
        self._count += self._step_spin.value()
        self._count_label.setText(str(self._count))
        self.value_changed.emit(old, self._count)

    def _decrement(self):
        old = self._count
        self._count -= self._step_spin.value()
        self._count_label.setText(str(self._count))
        self.value_changed.emit(old, self._count)

    def _reset(self):
        old = self._count
        self._count = 0
        self._count_label.setText("0")
        self.value_changed.emit(old, self._count)

    def _update_status(self, old_value: int, new_value: int):
        self._status_label.setText(f"{old_value} -> {new_value}")


def main():
    app = QApplication(sys.argv)
    window = CounterWidget()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()