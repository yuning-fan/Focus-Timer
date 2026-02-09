import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, Qt
from core_logic import TimerBackend
from ui_components import OceanFrame

class OceanTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.backend = TimerBackend(focus_minutes=25)
        self.is_running = False
        self.is_collapsed = False
        self.is_dragging = False
        self.init_window()

    def init_window(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 350)

        self.ui = OceanFrame(self)
        self.ui.setGeometry(0, 0, 300, 350)
        self.ui.start_btn.clicked.connect(self.toggle_timer)
        self.ui.reset_btn.clicked.connect(self.reset_timer)
        self.ui.quit_btn.clicked.connect(self.close)

        self.logic_timer = QTimer(self)
        self.logic_timer.timeout.connect(self.on_tick)

    def on_tick(self):
        if self.backend.tick():
            self.ui.timer_label.setText(self.backend.get_time_str())
        else:
            self.backend.save_data(25)
            self.expand_ui()
            self.ui.whale_label.setText("🥳")
            self.logic_timer.stop()
            self.is_running = False

    def toggle_timer(self):
        if not self.is_running:
            self.is_running = True
            self.ui.start_btn.setText("暂停")
            self.collapse_ui()
            self.logic_timer.start(1000)
        else:
            self.is_running = False
            self.ui.start_btn.setText("开始专注")
            self.expand_ui()
            self.logic_timer.stop()

    def collapse_ui(self):
        self.is_collapsed = True
        self.ui.btn_widget.hide()
        self.ui.timer_label.hide()
        self.ui.quit_btn.hide()
        self.ui.whale_label.setText("📖")
        self.setFixedSize(160, 160)
        self.ui.setGeometry(0, 0, 160, 160)
        self.ui.update_bubble_style(True)

    def expand_ui(self):
        self.is_collapsed = False
        self.setFixedSize(300, 350)
        self.ui.setGeometry(0, 0, 300, 350)
        self.ui.btn_widget.show()
        self.ui.timer_label.show()
        self.ui.quit_btn.show()
        self.ui.update_bubble_style(False)

    def enterEvent(self, event):
        if self.is_running and self.is_collapsed:
            self.ui.whale_label.hide()
            self.ui.timer_label.show()

    def leaveEvent(self, event):
        if self.is_running and self.is_collapsed:
            self.ui.timer_label.hide()
            self.ui.whale_label.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.globalPosition().toPoint()
            self.relative_pos = self.drag_start_pos - self.frameGeometry().topLeft()
            self.is_dragging = False

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if (event.globalPosition().toPoint() - self.drag_start_pos).manhattanLength() > 3:
                self.is_dragging = True
                self.move(event.globalPosition().toPoint() - self.relative_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.is_dragging and self.is_collapsed:
                self.expand_ui()

    def reset_timer(self):
        self.logic_timer.stop()
        self.is_running = False
        self.backend.reset()
        self.ui.timer_label.setText("25:00")
        self.ui.start_btn.setText("开始专注")
        self.expand_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OceanTimerApp()
    window.show()
    sys.exit(app.exec())