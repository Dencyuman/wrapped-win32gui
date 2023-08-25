from typing import Optional
from logging import Logger

import win32gui
import win32process

from .window import Window

class Desktop:
    def __init__(self, logger: Optional[Logger] = None):
        win32gui.set_logger(logger)

    def get_all_windows(self) -> list[Window]:
        results = []
        win32gui.EnumWindows(lambda hwnd, results: results.append(Window(hwnd)), results)
        return results

    def get_windows_by_name(self, name) -> list[Window]:
        def _callback(hwnd, results):
            if name in win32gui.GetWindowText(hwnd):
                results.append(Window(hwnd))
        results = []
        win32gui.EnumWindows(_callback, results)
        return results

    def get_windows_by_class(self, class_name) -> list[Window]:
        def _callback(hwnd, results):
            if class_name in win32gui.GetClassName(hwnd):
                results.append(Window(hwnd))
        results = []
        win32gui.EnumWindows(_callback, results)
        return results

    def get_windows_by_pid(self, pid) -> list[Window]:
        def _callback(hwnd, results):
            _, process_id = win32process.GetWindowThreadProcessId(hwnd)
            if process_id == pid:
                results.append(Window(hwnd))
        results = []
        win32gui.EnumWindows(_callback, results)
        return results

    def get_all_top_visibile_windows(self) -> list[Window]:
        def callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                results.append(Window(hwnd))
        results = []
        win32gui.EnumWindows(callback, results)
        return results