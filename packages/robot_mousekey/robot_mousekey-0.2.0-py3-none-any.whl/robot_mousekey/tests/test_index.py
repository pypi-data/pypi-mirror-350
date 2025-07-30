import time

from ..index import mouse_click, mouse_move, mouse_scroll, mouse_drag, keyboard_hotkey


def test_mouse_click():
    mouse_click(60, 10)


def test_mouse_move():
    mouse_move(1800, 900, duration=5, tween="easeOutBounce")


def test_mouse_scroll():
    time.sleep(5)
    mouse_scroll(-1000)


def test_mouse_drag():
    time.sleep(5)
    mouse_drag((734, 402), (1423, 748), duration=2, tween="easeOutCubic")


def test_keyboard_hotkey():
    keyboard_hotkey("win;d")
