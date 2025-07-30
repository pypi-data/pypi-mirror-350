import threading
import time
import tkinter as tk
from tkinter.font import Font


class MainWindow:
    def __init__(self, width, height, x, y, text, click_func):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text

        self.root = None
        self.main_window = None
        self.label_window = None
        self.click_func = click_func
        self.init = False

        threading.Thread(target=self.init_window, daemon=True).start()

    def init_window(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏根窗口
        # 创建主窗口
        self.main_window = tk.Toplevel(self.root)
        self.main_window.overrideredirect(True)  # 去除窗口边框
        self.main_window.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.main_window.config(bg="#ADD8E6")  # 设置浅蓝色背景
        self.main_window.attributes("-alpha", 0.3)  # 设置窗口透明度
        self.main_window.wm_attributes("-topmost", 1)
        self.main_window.bind("<Control-Button-1>", self.click_func)

        # 设置红色边框
        self.main_window.config(highlightbackground="red", highlightthickness=2)

        # 创建标签窗口
        self.label_window = LabelWindow(self.main_window, self.text)

        # 绑定窗口移动事件
        self.main_window.bind("<Configure>", self.on_configure)
        self.text = ""
        self.hide()
        self.init = True
        self.root.mainloop()

    def on_configure(self, event=None):
        # 获取主窗口的新位置
        new_x = self.main_window.winfo_x()
        new_y = self.main_window.winfo_y()

        if new_y < 100:  # 如果窗口靠近顶部
            self.label_window.set_label(self.text)
            self.label_window.set_position(new_x, new_y + self.height)
        else:  # 如果窗口靠近底部或其他位置
            self.label_window.set_label(self.text)
            self.label_window.set_position(new_x, new_y - self.label_window.height)

    def ensure_init(self):
        while not self.init:
            time.sleep(0.1)

    def update_position(self, x, y, width, height, text, delay: float = 2):
        self.ensure_init()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.main_window.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.on_configure()
        self.show()
        time.sleep(delay)
        self.hide()

    def highlight(self, x, y, width, height, text, times=3):
        self.update_position(x, y, width, height, text, delay=0.5)
        for _ in range(times):
            time.sleep(0.1)
            self.show()
            time.sleep(0.5)
            self.hide()

    def hide(self):
        self.main_window.withdraw()
        self.label_window.hide()

    def show(self):
        self.main_window.deiconify()
        self.label_window.show()


class LabelWindow:
    def __init__(self, parent, text):
        self.parent = parent
        self.text = text
        self.height = 20  # 默认高度

        # 创建标签窗口
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)  # 去除窗口边框
        self.window.config(bg="black")
        self.window.attributes("-alpha", 0.6)
        self.window.wm_attributes("-topmost", 1)

        self.font = Font(size=10)
        # 创建标签
        self.label = tk.Label(
            self.window,
            text=self.text,
            bg="black",
            fg="white",
            anchor="w",
            justify="left",
            font=self.font,
        )
        self.label.pack(pady=0)

        # 调整窗口大小
        self.window.update_idletasks()
        self.width = 200
        self.window.geometry(f"{self.width}x{self.height}")

    def set_position(self, x, y):
        text_width = self.font.measure(self.text) + 20
        self.window.geometry(f"{text_width}x{self.height}+{x}+{y}")

    def set_label(self, text):
        self.text = text
        if len(text) > 0:
            self.label.config(text=text)
            self.window.deiconify()
        else:
            self.window.withdraw()

    def hide(self):
        self.window.withdraw()

    def show(self):
        if len(self.text) > 0:
            self.label.config(text=self.text)
            self.window.deiconify()
        else:
            self.window.withdraw()


if __name__ == "__main__":
    from robot_base import TipWindow

    main_window = MainWindow(
        width=200,
        height=200,
        x=300,
        y=300,
        text="标记元素的位置和类型",
        click_func=lambda event: print("点击了窗口"),
    )
    tip_window = TipWindow(
        text="按下 Esc 退出拾取\n按下 F1 切换 Web 元素拾取模式\n按下 F2 切换 Windows 应用拾取模式\n按下 F3 切换 Java 应用拾取模式"
    )
    main_window.update_position(100, 100, 300, 400, text="111")
    time.sleep(2)
    main_window.update_position(200, 400, 300, 400, text="111")
    time.sleep(2)
    main_window.update_position(
        200, 400, 300, 400, text="ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    time.sleep(2)
    tip_window.hide()
    main_window.highlight(
        500, 400, 500, 200, text="ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    time.sleep(2)
