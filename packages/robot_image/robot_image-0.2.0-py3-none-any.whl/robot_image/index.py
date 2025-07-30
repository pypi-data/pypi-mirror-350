import json
import os
import random
import time
import tkinter

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from robot_base import TemporaryException, func_decorator, log_decorator


@log_decorator
def screen_size(**kwargs):
    """
    获取屏幕大小
    :return:
    """
    return pyautogui.size()


@log_decorator
def get_dpi(**kwargs):
    root = tkinter.Tk()
    dpi_value = root.winfo_fpixels("1i")
    root.destroy()
    return dpi_value


@log_decorator
@func_decorator
def find_target_position(
    target_id,
    **kwargs,
):
    """
    查找目标图片位置
    :param target_id:目标图片id
    :return: 目标位置（左上角x坐标，左上角y坐标，右下角x坐标，右下角y坐标）
    """
    threshold = float(target_id["threshold"])
    gray_style = True
    match_type = target_id["match_type"]
    try:
        if match_type == "template":
            return find_target_position_by_template(
                target_id["image_path"], gray_style, threshold
            )
        else:
            return find_target_position_by_sift(target_id["image_path"], threshold)
    except:
        return None


def find_target_position_by_template(
    target_path: str, gray_style: bool, threshold: float = 0.9
):
    """
    查找目标图片位置
    :param target_path:目标图片路径
    :param gray_style: 是否灰度模式
    :param threshold: 匹配阈值
    :return: 目标位置（左上角x坐标，左上角y坐标，右下角x坐标，右下角y坐标）
    """
    screen_scale = 1
    target = cv2.imread(
        target_path, cv2.IMREAD_GRAYSCALE if gray_style else cv2.COLOR_RGB2BGR
    )
    im = ImageGrab.grab()
    im.save("screen.png")
    temp = cv2.imread(
        r"screen.png", cv2.IMREAD_GRAYSCALE if gray_style else cv2.COLOR_RGB2BGR
    )
    os.remove("screen.png")
    target_height, target_width = target.shape[:2]
    temp_height, temp_width = temp.shape[:2]
    # print("目标图宽高：" + str(target_width) + "-" + str(target_height))
    # print("模板图宽高：" + str(temp_width) + "-" + str(temp_height))

    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scale_temp = cv2.resize(
        temp, (int(temp_width / screen_scale), int(temp_height / screen_scale))
    )
    scale_temp_height, scale_temp_width = scale_temp.shape[:2]
    # print("缩放后模板图宽高：" + str(scale_temp_width) + "-" + str(scale_temp_height))
    # 匹配图片
    res = cv2.matchTemplate(scale_temp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        # 计算出中心点
        top_left = max_loc
        bottom_right = (top_left[0] + target_width, top_left[1] + target_height)
        return top_left[0], top_left[1], bottom_right[0], bottom_right[1]
    else:
        return None


def find_target_position_by_sift(target_path: str, threshold: float = 0.9):
    """
    查找目标图片位置(根据图片SIFT特征点进行匹配)
    :param target_path:目标图片路径
    :param threshold: 匹配阈值
    :return: 目标位置（左上角x坐标，左上角y坐标，右下角x坐标，右下角y坐标）
    """
    return ImageClicker(target_path, threshold).find_image()


@log_decorator
@func_decorator
def click_target(
    target_id,
    show_mouse_position=False,
    button="left",
    click_type="single",
    position="center",
    **kwargs,
):
    """
    点击目标图片
    :param target_id: 图片id
    :param show_mouse_position:是否显示鼠标移动轨迹
    :param button:鼠标按钮,左键(left)，右键(right)，中键(middle)
    :param click_type:点击方式，双击(double)，单击(single)，按下(down)，弹起(up)
    :param position:点击位置，正中心(center)，随机(random)，指定位置(normal)
    :return:
    """
    target_position = find_target_position(target_id)

    if target_position is None:
        raise TemporaryException(f"目标图片:{target_id["image_path"]}未找到")
    x1, y1, x2, y2 = target_position
    target_x = x1 + (x2 - x1) / 2
    target_y = y1 + (y2 - y1) / 2
    if position == "random":
        target_x = x1 + random.Random().randint(0, x2 - x1)
        target_y = y1 + random.Random().randint(0, y2 - y1)
    elif position == "normal":
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        target_x = x1 + x
        target_y = y1 + y
    if show_mouse_position:
        pyautogui.moveTo(target_x, target_y, duration=0.5)
    if click_type == "double":
        pyautogui.doubleClick(target_x, target_y, button=button)
    elif click_type == "down":
        pyautogui.mouseDown(target_x, target_y, button=button)
    elif click_type == "up":
        pyautogui.mouseUp(target_x, target_y, button=button)
    else:
        pyautogui.click(target_x, target_y, button=button)


@log_decorator
def wait_target(target_id, wait_result="display", timeout=1000, **kwargs):
    """
    等待目标图片出现
    :param target_id:图片id
    :param wait_result:等待结果,出现(display),消失(disappear)
    :param timeout:超时时间(秒)
    :return:
    """
    start = time.perf_counter()
    while True:
        if wait_result == "display":
            if find_target_position(target_id) is not None:
                return True
        else:
            if find_target_position(target_id) is None:
                return True
        remain = start + timeout - time.perf_counter()
        if remain > 0:
            time.sleep(min(remain, 0.5))
        if remain <= 0:
            return False


class ImageClicker:
    def __init__(self, target_image_path, match_threshold=0.75):
        self.target_image_path = target_image_path
        self.match_threshold = match_threshold
        self.target_image = cv2.imread(self.target_image_path)
        self.sift = cv2.SIFT_create()
        self.kp1, self.des1 = self.sift.detectAndCompute(self.target_image, None)

    def find_image(self):
        try:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            kp2, des2 = self.sift.detectAndCompute(screenshot, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(self.des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < self.match_threshold * n.distance:
                    good.append([m])
            if len(good) > 0:
                src_pts = np.float32(
                    [self.kp1[m[0].queryIdx].pt for m in good]
                ).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m[0].trainIdx].pt for m in good]).reshape(
                    -1, 1, 2
                )
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                h, w = self.target_image.shape[:2]
                pts = np.float32(
                    [[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]
                ).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)

                return dst[0][0][0], dst[0][0][1], dst[2][0][0], dst[2][0][1]
        except Exception as e:
            print(f"点击失败：{e}")
        return None
