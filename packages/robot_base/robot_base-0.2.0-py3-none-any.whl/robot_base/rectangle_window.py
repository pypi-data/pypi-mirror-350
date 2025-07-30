import threading
import time
import tkinter as tk
from tkinter.font import Font


class RectangleWindow:
    def __init__(self, x, y, width, height, text="", color="black"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font = None

        self.root = None
        self.windows = []
        self.label_window = None
        self.label = None

        threading.Thread(target=self.init_window, daemon=True).start()

    def init_window(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏根窗口

        self.create_text()
        top_line = self.create_line(self.x, self.y, self.width, 2)
        bottom_line = self.create_line(self.x, self.y + self.height, self.width, 2)
        left_line = self.create_line(self.x, self.y, 2, self.height)
        right_line = self.create_line(self.x + self.width, self.y, 2, self.height + 2)

        self.windows = [
            top_line,
            bottom_line,
            left_line,
            right_line,
        ]
        self.hide_all()
        self.root.mainloop()

    def create_line(self, x, y, width, height):
        window = tk.Toplevel(self.root)
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.overrideredirect(True)
        window.configure(bg=self.color)

        # 使窗口置顶
        window.attributes("-topmost", True)

        return window

    def create_text(self):
        self.font = Font(size=10)
        self.label_window = tk.Toplevel(self.root)
        self.label_window.overrideredirect(True)  # 去除窗口边框
        self.label_window.config(bg="black")
        self.label_window.attributes("-alpha", 0.6)
        self.label_window.wm_attributes("-topmost", 1)

        self.label = tk.Label(
            self.label_window,
            text=self.text,
            bg="black",
            fg="white",
            anchor="w",
            justify="left",
            font=self.font,
        )
        self.label.pack(pady=0)
        if self.y > 30:
            self.label_window.geometry(f"200x20+{self.x}+{self.y-20}")
        else:
            self.label_window.geometry(f"200x20+{self.x}+{self.y+self.height}")

    def display_all(self):
        for window in self.windows:
            window.deiconify()
        if len(self.text) > 0:
            self.label_window.deiconify()

    def hide_all(self):
        for window in self.windows:
            window.withdraw()
        self.label_window.withdraw()

    def update_position(self, x, y, width, height, text=""):
        self.x = x
        self.y = 1 if (y < 0 and abs(y) < 5) else y
        self.width = width
        self.height = height
        self.text = text
        while len(self.windows) < 4:
            time.sleep(0.1)
        self.hide_all()
        self.windows[0].geometry(f"{self.width}x2+{self.x}+{self.y}")
        self.windows[1].geometry(f"{self.width}x2+{self.x}+{self.y+self.height}")
        self.windows[2].geometry(f"2x{self.height}+{self.x}+{self.y}")
        self.windows[3].geometry(f"2x{self.height}+{self.x+self.width}+{self.y}")
        if len(text) > 0:
            text_width = self.font.measure(self.text) + 20
            self.label.config(text=self.text)
            if self.y > 30:
                self.label_window.geometry(f"{text_width}x20+{self.x}+{self.y-20}")
            else:
                self.label_window.geometry(
                    f"{text_width}x20+{self.x}+{self.y+self.height}"
                )
        self.display_all()

    def highlight(self, times=3):
        for i in range(times):
            self.display_all()
            time.sleep(0.5)
            self.hide_all()
            time.sleep(0.1)

    def close_all(self):
        for window in self.windows:
            window.destroy()
        self.label_window.destroy()
        self.root.quit()


if __name__ == "__main__":

    rectangle = RectangleWindow(100, 100, 300, 400, text="", color="red")
    rectangle.update_position(0, 0, 100, 100)
    time.sleep(1)
    rectangle.update_position(300, 300, 100, 100, "测试")
    time.sleep(1)
    rectangle.update_position(400, 400, 10, 100, "测试")
    time.sleep(1)
    rectangle.update_position(0, 0, 10, 100, "测试")
    time.sleep(1)
    rectangle.update_position(30, 200, 800, 200, "测试")
    rectangle.highlight()
    rectangle.close_all()
    time.sleep(5)
