import os
import random
import time
import uuid

import psutil
import win32con
from robot_base import func_decorator, ParamException, TemporaryException, log_decorator
from uiautomation import uiautomation
from win32comext.shell import shellcon
from win32comext.shell.shell import ShellExecuteEx

from .find_by_xpath import find_element_by_xpath, find_elements_by_xpath


@log_decorator
@func_decorator
def open_app(**kwargs):
    if "executable_path" not in kwargs or not kwargs["executable_path"]:
        raise ParamException("应用可执行文件路径不能为空")
    executable_path = kwargs["executable_path"]
    work_dir = kwargs["work_dir"] if "work_dir" in kwargs else ""
    style = kwargs["style"] if "style" in kwargs else "default"
    params = kwargs.get("params", "")
    is_admin = kwargs.get("is_admin", False)
    if style == "max":
        show_type = win32con.SW_SHOWMAXIMIZED
    elif style == "min":
        show_type = win32con.SW_SHOWMINIMIZED
    elif style == "hide":
        show_type = win32con.SW_HIDE
    else:
        show_type = win32con.SW_SHOWNORMAL

    ShellExecuteEx(
        fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
        hwnd=None,
        lpVerb="runas" if is_admin else "",
        lpFile=executable_path,
        lpDirectory=work_dir,
        nShow=show_type,
        lpParameters=params,
    )


@log_decorator
@func_decorator
def close_app(**kwargs):
    if "window_type" not in kwargs:
        raise ParamException("参数异常")
    if kwargs["window_type"] == "process_name":
        pids = psutil.pids()
        pname = kwargs["pname"]
        for pid in pids:
            pro = psutil.Process(pid)
            if pname == pro.name() or pname + ".exe" == pro.name():
                pro.kill()
    else:
        control = __get_element(**kwargs)
        window = control.GetTopLevelControl()
        psutil.Process(window.ProcessId).kill()


@log_decorator
@func_decorator
def window_activate(**kwargs):
    control = __get_element(**kwargs)
    control.GetTopLevelControl().SetActive()


@log_decorator
@func_decorator
def set_window_visual_state(**kwargs):
    if "state" not in kwargs or not kwargs["state"]:
        raise ParamException("窗口状态不能为空")

    state = kwargs["state"]
    control = __get_element(**kwargs)
    if state == "min":
        control.ShowWindow(uiautomation.SW.Minimize)
    elif state == "normal":
        control.ShowWindow(uiautomation.SW.Normal)
    elif state == "max":
        control.ShowWindow(uiautomation.SW.Maximize)
    elif state == "hide":
        control.Hide()


@log_decorator
@func_decorator
def set_window_topmost(**kwargs):
    if "topmost" not in kwargs:
        raise ParamException("窗口状态不能为空")

    topmost = kwargs["topmost"]
    control = __get_element(**kwargs)
    control.GetTopLevelControl().SetTopmost(topmost)


@log_decorator
@func_decorator
def move_window(**kwargs):
    if "x" not in kwargs:
        raise ParamException("窗口X坐标不能为空")
    if "y" not in kwargs:
        raise ParamException("窗口Y坐标不能为空")
    x = kwargs["x"]
    y = kwargs["y"]

    control = __get_element(**kwargs)
    window = control.GetTopLevelControl()
    window.MoveWindow(
        x=int(x),
        y=int(y),
        width=window.BoundingRectangle.width(),
        height=window.BoundingRectangle.height(),
        repaint=False,
    )


@log_decorator
@func_decorator
def resize_window(**kwargs):
    if "width" not in kwargs or kwargs["width"] < 0:
        raise ParamException("窗口宽度值无效")
    if "height" not in kwargs or kwargs["height"] < 0:
        raise ParamException("窗口高度值无效")
    width = kwargs["width"]
    height = kwargs["height"]

    control = __get_element(**kwargs)
    window = control.GetTopLevelControl()
    window.MoveWindow(
        x=window.BoundingRectangle.left,
        y=window.BoundingRectangle.top,
        width=int(width),
        height=int(height),
        repaint=False,
    )


@log_decorator
@func_decorator
def close_window(**kwargs):
    control = __get_element(**kwargs)
    window = control.GetTopLevelControl()
    window.GetWindowPattern().Close()


@log_decorator
@func_decorator
def get_window_text(**kwargs):
    control = __get_element(**kwargs)
    window = control.GetTopLevelControl()
    return window.GetWindowText()


@log_decorator
@func_decorator
def get_element(**kwargs):
    if "windows_element" not in kwargs or not kwargs["windows_element"]:
        raise ParamException("元素标识不能为空")
    element = kwargs["windows_element"]
    parent_type = kwargs.get("parent_type", "desktop")
    if parent_type == "desktop":
        control = find_element_by_xpath(element)
    else:
        if "parent_control" not in kwargs or not kwargs["parent_control"]:
            raise ParamException("父元素对象不能为空")
        element = kwargs["windows_element"]
        parent_control = kwargs["parent_control"]
        control = find_element_by_xpath(element, parent_control)

    if control:
        return control
    else:
        raise TemporaryException(f"{element} 元素未找到")


@log_decorator
@func_decorator
def get_elements(**kwargs):
    if "windows_element" not in kwargs or not kwargs["windows_element"]:
        raise ParamException("元素标识不能为空")
    element = kwargs["windows_element"]
    parent_type = kwargs.get("parent_type", "desktop")
    if parent_type == "desktop":
        return find_elements_by_xpath(element)
    else:
        if "parent_control" not in kwargs or not kwargs["parent_control"]:
            raise ParamException("父元素对象不能为空")
        element = kwargs["windows_element"]
        parent_control = kwargs["parent_control"]
        return find_elements_by_xpath(element, parent_control)


def __get_element(**kwargs):
    if "locate_type" not in kwargs or not kwargs["locate_type"]:
        raise ParamException("定位元素方式不能为空")
    locate_type = kwargs["locate_type"]
    if locate_type == "windows_element":
        if "windows_element" not in kwargs or not kwargs["windows_element"]:
            raise ParamException("元素标识不能为空")
        element = kwargs["windows_element"]

        control = find_element_by_xpath(element)
    else:
        if "windows_control" not in kwargs or not kwargs["windows_control"]:
            raise ParamException("windows元素不能为空")
        control = kwargs["windows_control"]
    return control


@log_decorator
@func_decorator
def element_click(**kwargs):
    control = __get_element(**kwargs)
    button = kwargs.get("button", "left")
    simulate = kwargs.get("simulate", True)
    click_type = kwargs.get("click_type", "single")
    position = kwargs.get("position", "center")
    ratio_x = 0.5
    ratio_y = 0.5
    x = None
    y = None
    if position == "random":
        ratio_x = random.random()
        ratio_y = random.random()
    if position == "normal":
        x = int(kwargs.get("x", 0))
        y = int(kwargs.get("y", 0))

    if button == "left":
        if click_type == "single":
            control.Click(x=x, y=y, simulateMove=simulate, ratioX=0.5, ratioY=0.5)
        else:
            control.DoubleClick(
                x=x,
                y=y,
                simulateMove=simulate,
                ratioX=ratio_x,
                ratioY=ratio_y,
            )
    elif button == "middle":
        control.MiddleClick(
            x=x, y=y, simulateMove=simulate, ratioX=ratio_x, ratioY=ratio_y
        )
    elif button == "right":
        control.RightClick(
            x=x, y=y, simulateMove=simulate, ratioX=ratio_x, ratioY=ratio_y
        )


@log_decorator
@func_decorator
def element_hover(**kwargs):
    control = __get_element(**kwargs)
    simulate = kwargs.get("simulate", True)
    position = kwargs.get("position", "center")
    ratio_x = 0.5
    ratio_y = 0.5
    x = None
    y = None
    if position == "random":
        ratio_x = random.random()
        ratio_y = random.random()
    if position == "normal":
        x = int(kwargs.get("x", 0))
        y = int(kwargs.get("y", 0))
    control.MoveCursorToInnerPos(
        x=x, y=y, ratioX=ratio_x, ratioY=ratio_y, simulateMove=simulate
    )


@log_decorator
@func_decorator
def element_input(**kwargs):
    control = __get_element(**kwargs)
    content = kwargs.get("content", "")
    append = kwargs.get("append", False)
    click = kwargs.get("click", True)
    input_method = kwargs.get("input_method", "simulate")
    if input_method == "direct":
        if click:
            control.Click()
        if append:
            content = control.GetValuePattern().Value + content
        control.GetValuePattern().SetValue(content)
    elif input_method == "simulate":
        if click:
            control.Click(simulateMove=True)
        if append:
            uiautomation.SendKey(key=uiautomation.SpecialKeyNames["END"])
        else:
            uiautomation.SendKey(key=uiautomation.SpecialKeyNames["END"])
            uiautomation.SendKeys(text="{Ctrl}a")
            uiautomation.SendKey(key=uiautomation.SpecialKeyNames["DELETE"])
        uiautomation.SendKeys(content)
    elif input_method == "paste":
        if click:
            control.Click(simulateMove=False)
        if append:
            uiautomation.SendKey(key=uiautomation.SpecialKeyNames["END"])
        else:
            uiautomation.SendKey(key=uiautomation.SpecialKeyNames["END"])
            uiautomation.SendKeys(text="{Ctrl}a")
            uiautomation.SendKey(key=uiautomation.SpecialKeyNames["DELETE"])
        uiautomation.SetClipboardText(content)
        uiautomation.SendKeys(text="{Ctrl}v")


@log_decorator
@func_decorator
def get_element_text(**kwargs) -> str:
    control = __get_element(**kwargs)
    if control.GetPattern(uiautomation.PatternId.TextPattern):
        return control.GetPattern(
            uiautomation.PatternId.TextPattern
        ).DocumentRange.GetText()
    elif control.GetPattern(uiautomation.PatternId.ValuePattern):
        return control.GetPattern(uiautomation.PatternId.ValuePattern).Value
    else:
        return control.Name


@log_decorator
@func_decorator
def element_capture(**kwargs):
    control = __get_element(**kwargs)
    save_to_clip = kwargs.get("save_to_clip", False)
    if save_to_clip:
        uiautomation.SetClipboardBitmap(control.ToBitmap())
    else:
        save_dir = kwargs.get("save_dir", "")
        if not save_dir:
            raise ParamException("截图保存目录不能为空")
        random_name = kwargs.get("random_name", True)
        if random_name:
            save_path = os.path.join(save_dir, uuid.uuid4().hex + ".png")
        else:
            file_name = kwargs.get("file_name", "")
            if not file_name:
                raise ParamException("图片名称不能为空")
            save_path = os.path.join(save_dir, file_name + ".png")
            override = kwargs.get("override", True)
            if not override and os.path.exists(save_path):
                return save_path
        control.CaptureToImage(savePath=save_path)
        return save_path


@log_decorator
@func_decorator
def element_set_combox(**kwargs):
    control = __get_element(**kwargs)
    select_type = kwargs.get("select_type", "by_label")
    if select_type == "by_label":
        selected_value = kwargs.get("selected_value")
        control.Select(itemName=selected_value)
    else:
        selected_index = kwargs.get("selected_index")
        index = {"value": 0}

        def condition(name):
            if index["value"] == selected_index:
                return True
            else:
                index["value"] = index["value"] + 1
                return False

        control.Select(condition=condition)


@log_decorator
@func_decorator
def element_set_checkbox(**kwargs):
    control = __get_element(**kwargs)
    operate = kwargs.get("operate", "checked")
    state = control.GetTogglePattern().ToggleState
    if operate == "checked" and state == 0:
        control.GetTogglePattern().Toggle()
    elif operate == "unchecked" and state == 1:
        control.GetTogglePattern().Toggle()
    elif operate == "toggle":
        control.GetTogglePattern().Toggle()


@log_decorator
@func_decorator
def scroll_element(**kwargs):
    control = __get_element(**kwargs)
    scroll_type = kwargs.get("scroll_type", "absolute_position")
    if control.GetPattern(uiautomation.PatternId.ScrollPattern):
        scroll_pattern = control.GetScrollPattern()
        horizontal = kwargs.get("horizontal", 0)
        vertical = kwargs.get("vertical", 0)
        if scroll_type == "absolute_position":
            scroll_pattern.Scroll(
                horizontalAmount=int(horizontal), verticalAmount=int(vertical)
            )
        else:
            scroll_pattern.SetScrollPercent(
                horizontalPercent=float(horizontal), verticalPercent=float(vertical)
            )
    else:
        raise Exception("元素不支持滚动")


@log_decorator
@func_decorator
def wait_element(**kwargs):
    if "windows_element" not in kwargs or not kwargs["windows_element"]:
        raise ParamException("元素标识不能为空")
    element = kwargs["windows_element"]
    display = kwargs.get("display", "display")
    wait_time = kwargs.get("wait_time", 30)
    start = uiautomation.ProcessTime()

    while True:
        try:
            control = find_element_by_xpath(element)
        except:
            control = None
        if display == "display" and control:
            return True
        if display != "display" and not control:
            return True
        remain = start + wait_time - uiautomation.ProcessTime()
        if remain > 0:
            time.sleep(min(remain, 0.5))
        else:
            return False


@log_decorator
def mouse_move(x, y, move_speed=1, **kwargs):
    """
    鼠标移动到指定位置
    :param x:
    :param y:
    :param move_speed:
    :param kwargs:
    :return:
    """
    x = int(x)
    y = int(y)
    move_speed = int(move_speed)
    uiautomation.MoveTo(x, y, move_speed)


@log_decorator
def mouse_up_down(x, y, mouse_type, button, **kwargs):
    """
    鼠标在指定位置按下或抬起
    :param x:
    :param y:
    :param mouse_type:
    :param button:
    :param kwargs:
    :return:
    """
    x = int(x)
    y = int(y)
    if mouse_type == "down":
        if button == "left":
            uiautomation.PressMouse(x, y)
        elif button == "right":
            uiautomation.RightPressMouse(x, y)
        elif button == "middle":
            uiautomation.MiddlePressMouse(x, y)
    elif mouse_type == "up":
        if button == "left":
            uiautomation.ReleaseMouse()
        elif button == "right":
            uiautomation.RightReleaseMouse()
        elif button == "middle":
            uiautomation.MiddleReleaseMouse()


@log_decorator
def mouse_click(x, y, click_type, button, **kwargs):
    """
    点击鼠标
    :param x:
    :param y:
    :param click_type:
    :param button:
    :param kwargs:
    :return:
    """
    x = int(x)
    y = int(y)
    if click_type == "single":
        if button == "left":
            uiautomation.Click(x, y)
        elif button == "right":
            uiautomation.RightClick(x, y)
        elif button == "middle":
            uiautomation.MiddleClick(x, y)
    elif click_type == "double":
        if button == "left":
            uiautomation.Click(x, y, uiautomation.GetDoubleClickTime() * 1.0 / 2000)
            uiautomation.Click(x, y)
        elif button == "right":
            uiautomation.RightClick(
                x, y, uiautomation.GetDoubleClickTime() * 1.0 / 2000
            )
            uiautomation.RightClick(x, y)
        elif button == "middle":
            uiautomation.MiddleClick(
                x, y, uiautomation.GetDoubleClickTime() * 1.0 / 2000
            )
            uiautomation.MiddleClick(x, y)


@log_decorator
def mouse_scroll(direction, wheel_times, **kwargs):
    """
    鼠标滚轮滚动
    :param direction:
    :param wheel_times:
    :param kwargs:
    :return:
    """
    wheel_times = int(wheel_times)
    if direction == "up":
        uiautomation.WheelUp(wheel_times)
    elif direction == "down":
        uiautomation.WheelDown(wheel_times)


@log_decorator
def hotkey(key, interval=0.01, **kwargs):
    interval = float(interval)
    uiautomation.SendKeys(key, interval)
