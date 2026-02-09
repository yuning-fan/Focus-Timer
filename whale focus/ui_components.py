from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class OceanFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("MainContainer")
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)

        # 鲸鱼图标
        self.whale_label = QLabel("🐳")
        self.whale_label.setFont(QFont("Segoe UI Emoji", 70))
        self.whale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.whale_label)

        # 计时器
        self.timer_label = QLabel("25:00")
        self.timer_label.setFont(QFont("Consolas", 40, 700))
        self.timer_label.setStyleSheet("color: #1a2980; border: none;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.hide()
        self.layout.addWidget(self.timer_label)

        # 按钮区
        self.btn_widget = QWidget()
        self.btn_layout = QHBoxLayout(self.btn_widget)
        self.start_btn = QPushButton("开始专注")
        self.reset_btn = QPushButton("重置")
        self.btn_layout.addWidget(self.start_btn)
        self.btn_layout.addWidget(self.reset_btn)
        self.layout.addWidget(self.btn_widget)

    def update_bubble_style(self, is_collapsed):
        radius = 80 if is_collapsed else 30
        self.setStyleSheet(f"""
            #MainContainer {{
                background: rgba(224, 247, 255, 230);
                border: 2px solid #3498db;
                border-radius: {radius}px;
            }}
        """)