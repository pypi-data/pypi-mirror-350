import base64
import json
import tkinter as tk
import tkinter.filedialog
from io import BytesIO

from PIL import ImageGrab


# 用来显示全屏幕截图并响应二次截图的窗口类
class Screenshot:

    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-fullscreen", True)
        self.root.title("截图")
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.sel = False
        self.move = False
        self.resize = False
        self.last_draw = None
        self.text = None
        self.threshold = 5

        # 屏幕尺寸
        self.canvas = tkinter.Canvas(self.root, bg="black")
        # 显示全屏截图，在全屏截图上进行区域截图
        self.canvas.config(highlightthickness=0)

        def on_esc(event):
            self.root.quit()

        self.root.bind("<Escape>", on_esc)

        def on_enter(event):
            if self.last_draw:
                x1, y1, x2, y2 = self.canvas.coords(self.last_draw)
                x1 = max(x1, 0)
                y1 = max(y1, 0)
                x2 = min(x2, self.root.winfo_screenwidth())
                y2 = min(y2, self.root.winfo_screenheight())
                try:
                    self.canvas.delete(self.last_draw)
                    self.last_draw = None
                except Exception as e:
                    pass
                self.root.withdraw()
                pic = ImageGrab.grab((x1 + 1, y1 + 1, x2 - 1, y2 - 1))
                image_data = BytesIO()
                pic.save(image_data, format="JPEG")
                image_data_bytes = image_data.getvalue()
                encoded_image = base64.b64encode(image_data_bytes).decode("utf-8")
                image_map = {
                    "image": encoded_image,
                    "left": x1,
                    "top": y1,
                    "right": x2,
                    "bottom": y2,
                }
                print(json.dumps(image_map))
                # pic.save("capture.png")
                # 关闭当前窗口
                self.root.quit()

        self.root.bind("<Return>", on_enter)
        self.root.bind("<Double-1>", on_enter)

        # 鼠标左键按下的位置
        def on_left_button_down(event):
            if not self.last_draw:
                self.X.set(event.x)
                self.Y.set(event.y)
                # 开始截图
                self.sel = True
            else:
                x1, y1, x2, y2 = self.canvas.coords(self.last_draw)
                if (
                    in_threshold(
                        (event.x, event.y),
                        self.canvas.coords(self.last_draw),
                        self.threshold,
                    )
                    != 0
                ):
                    self.resize = True
                    if event.x < (x1 + x2) / 2:
                        self.X.set(x2)
                    else:
                        self.X.set(x1)
                    if event.y < (y1 + y2) / 2:
                        self.Y.set(y2)
                    else:
                        self.Y.set(y1)
                if (
                    x1 + self.threshold < event.x < x2 - self.threshold
                    and y1 + self.threshold < event.y < y2 - self.threshold
                ):
                    self.root.config(cursor="fleur")
                    self.move = True

        self.canvas.bind("<Button-1>", on_left_button_down)

        # 鼠标左键移动，显示选取的区域
        def on_left_button_move(event):
            if self.sel:
                try:
                    # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                    self.canvas.delete(self.last_draw)
                except Exception as e:
                    pass
                self.last_draw = self.canvas.create_rectangle(
                    self.X.get(), self.Y.get(), event.x, event.y, outline="red"
                )
                try:
                    # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                    self.canvas.delete(self.text)
                except Exception as e:
                    pass
                x1, y1, x2, y2 = self.canvas.coords(self.last_draw)
                self.text = self.canvas.create_text(
                    event.x,
                    event.y,
                    text=f"Rect{(x1, y1, x2, y2)}\nEsc退出截图\n双击或Enter完成截图",
                    fill="red",
                    anchor="nw",
                )
            if self.move:
                x = event.x
                y = event.y
                x1, y1, x2, y2 = self.canvas.coords(self.last_draw)
                # 更新矩形的位置
                rect_x1 = x - (x2 - x1) / 2
                rect_y1 = y - (y2 - y1) / 2
                self.canvas.coords(
                    self.last_draw,
                    rect_x1,
                    rect_y1,
                    rect_x1 + (x2 - x1),
                    rect_y1 + (y2 - y1),
                )

            if self.resize:
                try:
                    # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                    self.canvas.delete(self.last_draw)
                except Exception as e:
                    pass
                self.last_draw = self.canvas.create_rectangle(
                    self.X.get(), self.Y.get(), event.x, event.y, outline="red"
                )

        self.canvas.bind("<B1-Motion>", on_left_button_move)

        def on_mouse_move(event):
            if not self.sel and not self.move and self.last_draw:
                if (
                    in_threshold(
                        (event.x, event.y),
                        self.canvas.coords(self.last_draw),
                        self.threshold,
                    )
                    == 1
                ):
                    self.root.config(cursor="sizing")
                else:
                    self.root.config(cursor="arrow")

        self.canvas.bind("<Motion>", on_mouse_move)

        # 获取鼠标左键抬起的位置，保存区域截图
        def on_left_button_up(event):
            if self.sel:
                self.sel = False
                try:
                    self.canvas.delete(self.last_draw)
                except Exception as e:
                    pass
                self.last_draw = self.canvas.create_rectangle(
                    self.X.get(), self.Y.get(), event.x, event.y, outline="red"
                )

            if self.move or self.resize:
                self.move = False
                self.resize = False
                self.root.config(cursor="arrow")

            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(self.text)
            except Exception as e:
                pass
            x1, y1, x2, y2 = self.canvas.coords(self.last_draw)
            x = x2
            y = y2
            if y > self.root.winfo_screenheight() - 100:
                x = x1
                y = y1 - 50
            self.text = self.canvas.create_text(
                x,
                y,
                text=f"Rect{(x1, y1, x2, y2)}\nEsc退出截图\n双击或Enter完成截图",
                fill="red",
                anchor="nw",
            )

        self.canvas.bind("<ButtonRelease-1>", on_left_button_up)

        # 让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.root.mainloop()


def in_threshold(point, rect, threshold):
    x, y = point
    x1, y1, x2, y2 = rect
    if (
        x1 - threshold < x < x1 + threshold or x2 - threshold < x < x2 + threshold
    ) and (y1 - threshold < y < y1 + threshold or y2 - threshold < y < y2 + threshold):
        return 1
    return 0
