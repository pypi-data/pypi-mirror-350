import threading
import time
import tkinter as tk
from tkinter.font import Font


class TipWindow:
    def __init__(self, text="", width=300, height=80):
        self.width = width
        self.height = height
        self.text = text
        self.root = None
        self.window = None
        threading.Thread(target=self.init_window, daemon=True).start()

    def init_window(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏根窗口

        self.window = tk.Toplevel(self.root)
        self.window.overrideredirect(True)  # 去除窗口边框
        self.window.config(bg="black")
        self.window.attributes("-alpha", 0.8)
        self.window.wm_attributes("-topmost", 1)

        label = tk.Label(
            self.window,
            text=self.text,
            bg="black",
            fg="white",
            anchor="w",
            justify="left",
            font=Font(size=12),
        )
        label.pack(pady=2)

        self.window.bind("<Enter>", self.on_enter)
        self.window.update_idletasks()

        self.window.geometry(f"{self.width}x{self.height}+0+0")
        self.window.withdraw()
        self.root.mainloop()

    def on_enter(self, event=None):
        new_y = self.window.winfo_y()
        if new_y != 0:
            self.window.geometry(f"+{0}+{0}")
        else:
            # 移动到右下角
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.window.geometry(
                f"+{screen_width - self.width}+{screen_height-self.height-100}"
            )

    def show(self):
        while self.window is None:
            time.sleep(0.1)
        self.window.deiconify()

    def hide(self):
        while self.window is None:
            time.sleep(0.1)
        self.window.withdraw()


if __name__ == "__main__":
    tip_window = TipWindow(
        text="按下 Esc 退出拾取\n按下 F1 切换 Web 元素拾取模式\n按下 F2 切换 Windows 应用拾取模式\n按下 F3 切换 Java 应用拾取模式"
    )
    time.sleep(3)
