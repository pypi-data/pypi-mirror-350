import sys
from tkinter import Tk

from robot_image import find_target_position_by_template, find_target_position_by_sift


def find_target_position(
    target_path: str, gray_style: bool, threshold: float = 0.9, match_type="template"
):
    """
    查找目标图片位置
    :param target_path:目标图片路径
    :param gray_style: 是否灰度模式
    :param threshold: 匹配阈值
    :param match_type: 匹配方式，模板匹配(template),SIFT特征点匹配(sift)
    :return: 目标位置（左上角x坐标，左上角y坐标，右下角x坐标，右下角y坐标）
    """
    if match_type == "template":
        return find_target_position_by_template(target_path, gray_style, threshold)
    else:
        return find_target_position_by_sift(target_path, threshold)


def highlight_section(rect=(100, 100, 300, 200), color="red", duration=1):
    win = Tk()
    width, height, place_x, place_y = rect
    geometry_string = f"{width}x{height}+{place_x}+{place_y}"
    win.geometry(geometry_string)
    win.configure(background=color)
    win.overrideredirect(True)
    win.attributes("-alpha", 0.3)
    win.wm_attributes("-topmost", 1)
    win.after(duration * 1000, lambda: win.destroy())
    win.mainloop()
