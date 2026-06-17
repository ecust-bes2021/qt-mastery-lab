from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
)

import sys
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practicase GUI code test")
        self.resize(400,200)

        self._label = QLabel("输入后点击按钮")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._line_edit = QLineEdit()
        self._line_edit.setPlaceholderText("在这里输入一些文字")

        self._button = QPushButton("显示输入内容")

        layout = QVBoxLayout(self)
        layout.addWidget(self._label)
        layout.addWidget(self._line_edit)
        layout.addWidget(self._button)

        self._button.clicked.connect(self._on_btn_onclicked)
    
    def _on_btn_onclicked(self):
        text = self._line_edit.text().strip()
        if text:
            self._label.setText(f"你输入了：{text}")
        else:
            self._label.setText("输入的内容为空")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())      

if __name__ == "__main__":
    main()