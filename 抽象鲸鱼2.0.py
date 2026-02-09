import sys
import json
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont


class OceanTimer(QWidget):
    def __init__(self):
        super().__init__()
        # --- 数据初始化 ---
        self.focus_minutes = 25
        self.time_left = self.focus_minutes * 60
        self.is_running = False
        self.total_focus_minutes = 0
        self.is_collapsed = False

        self.data_file = "whale_stats.json"
        self.load_data()
        self.init_ui()

    def init_ui(self):
        # 窗口基础设置：置顶、无边框、透明背景
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 350)

        # 核心主容器 (所有的 UI 都在这里，控制圆角和背景)
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainContainer")
        self.main_frame.setGeometry(0, 0, 300, 350)
        self.update_style()

        self.layout = QVBoxLayout(self.main_frame)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        # 1. 鲸鱼图标
        self.whale_label = QLabel("🐳")
        self.whale_label.setFont(QFont("Segoe UI Emoji", 70))
        self.whale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.whale_label.setStyleSheet("background: transparent; border: none;")
        self.layout.addWidget(self.whale_label)

        # 2. 计时器文字 (默认隐藏)
        self.timer_label = QLabel("25:00")
        self.timer_label.setFont(QFont("Consolas", 40, 700))
        self.timer_label.setStyleSheet("color: #1a2980; background: transparent; border: none;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.hide()
        self.layout.addWidget(self.timer_label)

        # 3. 统计信息
        self.info_label = QLabel(f"等级: {self.get_level()} | {self.total_focus_minutes}m")
        self.info_label.setStyleSheet("color: #4a6fa5; font-size: 13px; background: transparent; border: none;")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_label)

        # 4. 按钮区域
        self.btn_widget = QWidget()
        self.btn_widget.setStyleSheet("background: transparent; border: none;")
        btn_layout = QHBoxLayout(self.btn_widget)

        self.start_btn = QPushButton("开始专注")
        self.reset_btn = QPushButton("重置")

        button_style = """
            QPushButton { 
                background: #3498db; color: white; border-radius: 12px; 
                padding: 8px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: #2980b9; }
        """
        self.start_btn.setStyleSheet(button_style)
        self.reset_btn.setStyleSheet(button_style)

        self.start_btn.clicked.connect(self.toggle_timer)
        self.reset_btn.clicked.connect(self.reset_timer)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.reset_btn)
        self.layout.addWidget(self.btn_widget)

        # 退出按钮 (右上角小叉)
        self.quit_btn = QPushButton("×", self.main_frame)
        self.quit_btn.setGeometry(260, 10, 30, 30)
        self.quit_btn.setStyleSheet("color: #e74c3c; border: none; font-size: 22px; background: transparent;")
        self.quit_btn.clicked.connect(self.close)

        self.logic_timer = QTimer(self)
        self.logic_timer.timeout.connect(self.tick)

    # --- 逻辑处理 ---

    def enterEvent(self, event):
        """鼠标移入：显示倒计时"""
        if self.is_running and self.is_collapsed:
            self.whale_label.hide()
            self.timer_label.show()

    def leaveEvent(self, event):
        """鼠标移出：恢复鲸鱼"""
        if self.is_running and self.is_collapsed:
            self.timer_label.hide()
            self.whale_label.show()

    def mousePressEvent(self, event):
        """点击整个窗口：如果在折叠状态，则展开"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_collapsed:
                self.expand_ui()
            # 记录拖拽位置
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """拖动窗口"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

    def toggle_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.setText("暂停")
            self.collapse_ui()
            self.logic_timer.start(1000)
        else:
            self.is_running = False
            self.start_btn.setText("继续")
            self.expand_ui()
            self.logic_timer.stop()

    def collapse_ui(self):
        self.is_collapsed = True
        self.btn_widget.hide()
        self.info_label.hide()
        self.quit_btn.hide()
        self.setFixedSize(160, 160)
        self.main_frame.setGeometry(0, 0, 160, 160)
        self.whale_label.setText("📖")
        self.update_style()

    def expand_ui(self):
        self.is_collapsed = False
        self.setFixedSize(300, 350)
        self.main_frame.setGeometry(0, 0, 300, 350)
        self.btn_widget.show()
        self.info_label.show()
        self.quit_btn.show()
        self.timer_label.show()
        self.whale_label.show()
        if not self.is_running:
            self.whale_label.setText("🐳")
        self.update_style()

    def tick(self):
        if self.time_left > 0:
            self.time_left -= 1
            m, s = divmod(self.time_left, 60)
            self.timer_label.setText(f"{m:02d}:{s:02d}")
        else:
            self.finish_focus()

    def finish_focus(self):
        self.logic_timer.stop()
        self.total_focus_minutes += self.focus_minutes
        self.save_data()
        self.expand_ui()
        self.is_running = False
        self.time_left = self.focus_minutes * 60
        self.whale_label.setText("🥳")
        self.timer_label.setText("完成!")

    def update_style(self):
        # 移除内部杂乱边框，只保留主气泡外框
        radius = 80 if self.is_collapsed else 30
        self.main_frame.setStyleSheet(f"""
            #MainContainer {{
                background: rgba(224, 247, 255, 230);
                border: 2px solid #3498db;
                border-radius: {radius}px;
            }}
        """)

    def get_level(self):
        if self.total_focus_minutes < 60: return "初生小鲸"
        return "海洋领主"

    def reset_timer(self):
        self.logic_timer.stop()
        self.is_running = False
        self.time_left = self.focus_minutes * 60
        self.timer_label.setText("25:00")
        self.expand_ui()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.total_focus_minutes = json.load(f).get("total_minutes", 0)

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump({"total_minutes": self.total_focus_minutes}, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OceanTimer()
    window.show()
    sys.exit(app.exec())