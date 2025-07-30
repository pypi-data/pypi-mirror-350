import pyautogui
import pytweening
from robot_base import log_decorator, ParamException


@log_decorator
def mouse_click(
    target_x,
    target_y,
    button="left",
    click_type="single",
    **kwargs,
):
    """
    鼠标点击
    :param target_x:点击坐标x
    :param target_y:点击坐标y
    :param button:鼠标按钮,左键(left)，右键(right)，中键(middle)
    :param click_type:点击方式，双击(double)，单击(single)，按下(down)，弹起(up)
    """

    if click_type == "double":
        pyautogui.doubleClick(target_x, target_y, button=button)
    elif click_type == "down":
        pyautogui.mouseDown(target_x, target_y, button=button)
    elif click_type == "up":
        pyautogui.mouseUp(target_x, target_y, button=button)
    else:
        pyautogui.click(target_x, target_y, button=button)


@log_decorator
def mouse_move(
    target_x,
    target_y,
    duration=0.0,
    tween="linear",
    **kwargs,
):
    """
    移动鼠标
    :param target_x:点击坐标x
    :param target_y:点击坐标y
    :param duration:移动的时间
    :param tween:移动的方式
    """
    tween_method = pytweening.linear
    tween_mapping = {
        "linear": pytweening.linear,
        "easeInQuad": pytweening.easeInQuad,
        "easeOutQuad": pytweening.easeOutQuad,
        "easeInOutQuad": pytweening.easeInOutQuad,
        "easeInCubic": pytweening.easeInCubic,
        "easeOutCubic": pytweening.easeOutCubic,
        "easeInOutCubic": pytweening.easeInCubic,
        "easeInQuart": pytweening.easeInQuart,
        "easeOutQuart": pytweening.easeOutQuart,
        "easeInOutQuart": pytweening.easeInOutQuart,
        "easeInQuint": pytweening.easeInQuint,
        "easeOutQuint": pytweening.easeOutQuint,
        "easeInOutQuint": pytweening.easeInOutQuint,
        "easeInSine": pytweening.easeInSine,
        "easeOutSine": pytweening.easeOutSine,
        "easeInOutSine": pytweening.easeInOutSine,
        "easeInExpo": pytweening.easeInExpo,
        "easeOutExpo": pytweening.easeOutExpo,
        "easeInOutExpo": pytweening.easeInOutExpo,
        "easeInCirc": pytweening.easeInCirc,
        "easeOutCirc": pytweening.easeOutCirc,
        "easeInOutCirc": pytweening.easeInOutCirc,
        "easeInElastic": pytweening.easeInElastic,
        "easeOutElastic": pytweening.easeOutElastic,
        "easeInOutElastic": pytweening.easeInOutElastic,
        "easeInBack": pytweening.easeInBack,
        "easeOutBack": pytweening.easeOutBack,
        "easeInOutBack": pytweening.easeInOutBack,
        "easeInBounce": pytweening.easeInBounce,
        "easeOutBounce": pytweening.easeOutBounce,
        "easeInOutBounce": pytweening.easeInOutBounce,
    }
    if tween in tween_mapping:
        tween_method = tween_mapping[tween]
    pyautogui.moveTo(target_x, target_y, duration=duration, tween=tween_method)


@log_decorator
def mouse_scroll(
    clicks,
    **kwargs,
):
    """
    鼠标滚轮操作
    :param clicks:滚动距离,负数向下，正数向上
    """

    pyautogui.scroll(clicks)


@log_decorator
def mouse_drag(
    src_pos,
    des_pos,
    duration=0.0,
    tween="linear",
    **kwargs,
):
    """
    鼠标滚轮操作
    :param src_pos:起点
    :param des_pos:终点
    :param duration:移动的时间
    :param tween:移动的方式
    """
    if type(src_pos) is not tuple:
        raise ParamException("起点类型不对")
    if type(des_pos) is not tuple:
        raise ParamException("终点类型不对")
    if len(src_pos) == 4:
        x1, y1, x2, y2 = src_pos
        pyautogui.moveTo(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2)
    else:
        pyautogui.moveTo(src_pos)
    tween_method = pytweening.linear
    tween_mapping = {
        "linear": pytweening.linear,
        "easeInQuad": pytweening.easeInQuad,
        "easeOutQuad": pytweening.easeOutQuad,
        "easeInOutQuad": pytweening.easeInOutQuad,
        "easeInCubic": pytweening.easeInCubic,
        "easeOutCubic": pytweening.easeOutCubic,
        "easeInOutCubic": pytweening.easeInCubic,
        "easeInQuart": pytweening.easeInQuart,
        "easeOutQuart": pytweening.easeOutQuart,
        "easeInOutQuart": pytweening.easeInOutQuart,
        "easeInQuint": pytweening.easeInQuint,
        "easeOutQuint": pytweening.easeOutQuint,
        "easeInOutQuint": pytweening.easeInOutQuint,
        "easeInSine": pytweening.easeInSine,
        "easeOutSine": pytweening.easeOutSine,
        "easeInOutSine": pytweening.easeInOutSine,
        "easeInExpo": pytweening.easeInExpo,
        "easeOutExpo": pytweening.easeOutExpo,
        "easeInOutExpo": pytweening.easeInOutExpo,
        "easeInCirc": pytweening.easeInCirc,
        "easeOutCirc": pytweening.easeOutCirc,
        "easeInOutCirc": pytweening.easeInOutCirc,
        "easeInElastic": pytweening.easeInElastic,
        "easeOutElastic": pytweening.easeOutElastic,
        "easeInOutElastic": pytweening.easeInOutElastic,
        "easeInBack": pytweening.easeInBack,
        "easeOutBack": pytweening.easeOutBack,
        "easeInOutBack": pytweening.easeInOutBack,
        "easeInBounce": pytweening.easeInBounce,
        "easeOutBounce": pytweening.easeOutBounce,
        "easeInOutBounce": pytweening.easeInOutBounce,
    }
    if tween in tween_mapping:
        tween_method = tween_mapping[tween]
    if len(des_pos) == 4:
        x1, y1, x2, y2 = des_pos
        pyautogui.dragTo(
            x1 + (x2 - x1) / 2,
            y1 + (y2 - y1) / 2,
            duration=duration,
            tween=tween_method,
        )
    else:
        pyautogui.dragTo(
            des_pos[0],
            des_pos[1],
            duration=duration,
            tween=tween_method,
        )


@log_decorator
def keyboard_type(
    message,
    interval=0.0,
    **kwargs,
):
    """
    键盘输入
    :param message:输入的内容
    :param interval:输入间隔
    """

    pyautogui.typewrite(message, interval=interval)


@log_decorator
def keyboard_hotkey(
    message: str,
    interval,
    **kwargs,
):
    """
    键盘快捷键
    :param message:输入的内容
    :param interval:按键间隔时间
    """
    keys = message.split(";")
    pyautogui.hotkey(*keys, interval=interval)
