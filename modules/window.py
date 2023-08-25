from typing import Optional

import win32gui
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
import itertools

from modules.utils import SWPFlags, ShowWindowCommands, Win32Constants


class Window:
    def __init__(self, hwnd):
        if isinstance(hwnd, str):
            hwnd = int(hwnd, 16)
        self.__hwnd: int = hwnd
        # parents_hwnds = []
        # while True:
        #     parents_hwnd = self.parent_hwnd
        #     if parents_hwnd is None:
        #         break
        #     parents_hwnds.append(parents_hwnd)
        # self.__level: int = len(parents_hwnds)
        # self.__hwnd_path: str = "/".join(parents_hwnds[::-1]) + "/" + str(self.hwnd).lstrip('/')

    def __str__(self) -> str:
        return f'[{self.hwnd}] {self.text}'

    def __repr__(self):
        return f'[{self.hwnd}] {self.text}'

    def to_dict(self):
        result = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not callable(value) and isinstance(type(self).__dict__.get(name), property):
                result[name] = value
        return result

    @property
    def hwnd(self) -> int:
        """ウィンドウハンドル
        
        Returns:
            int: ウィンドウハンドル
        """
        return self.__hwnd

    # @property
    # def level(self) -> int:
    #     """ウィンドウの階層レベル

    #     Returns:
    #         int: ウィンドウの階層レベル
    #     """
    #     return self.__level

    # @property
    # def hwnd_path(self) -> str:
    #     """ウィンドウのハンドルパス

    #     Returns:
    #         str: ウィンドウのハンドルパス
    #     """
    #     return self.__hwnd_path

    @property
    def text(self) -> str:
        """ウィンドウタイトル

        Returns:
            str: ウィンドウタイトル
        """
        return win32gui.GetWindowText(self.hwnd)

    @property
    def class_name(self) -> str:
        """ウィンドウクラス名

        Returns:
            str: ウィンドウクラス名
        """
        return win32gui.GetClassName(self.hwnd)

    @property
    def rect(self) -> tuple:
        """ウィンドウの位置とサイズ

        Returns:
            tuple: ウィンドウの位置とサイズ (left, top, right, bottom)
        """
        return win32gui.GetWindowRect(self.hwnd)

    @property
    def is_iconic(self) -> bool:
        """ウィンドウが最小化されているかどうか

        Returns:
            bool: 最小化フラグ
        """
        return bool(win32gui.IsIconic(self.hwnd))

    @property
    def parent_hwnd(self) -> int | None:
        """親ウィンドウのハンドル

        Returns:
            int | None: 親ウィンドウのハンドル
        """
        parent = win32gui.GetParent(self.hwnd)
        if parent == 0:
            return None
        return parent

    @property
    def parent(self) -> Optional["Window"]:
        """親ウィンドウ

        Returns:
            Optional[WindowObj]: 親ウィンドウ
        """
        parent = self.parent_hwnd
        if parent is None:
            return None
        return Window(parent)

    @property
    def children_hwnds(self) -> list[int]:
        """子ウィンドウのハンドル一覧

        Returns:
            list[int]: 子ウィンドウのハンドル一覧
        """
        children = []
        win32gui.EnumChildWindows(self.hwnd, lambda hwnd, children: children.append(hwnd), children)
        return children

    @property
    def children(self) -> list["Window"]:
        """子ウィンドウ一覧

        Returns:
            list[WindowObj]: 子ウィンドウ一覧
        """
        return [Window(hwnd) for hwnd in self.children_hwnds]

    @property
    def is_active(self) -> bool:
        """ウィンドウがアクティブかどうか

        Returns:
            bool: アクティブフラグ
        """
        return win32gui.GetForegroundWindow() == self.hwnd

    @property
    def client_rect(self) -> tuple:
        """クライアント領域の位置とサイズ

        Returns:
            tuple: クライアント領域の位置とサイズ (left, top, right, bottom)
        """
        return win32gui.GetClientRect(self.hwnd)

    @property
    def is_visible(self) -> bool:
        """ウィンドウが表示されているかどうか

        Returns:
            bool: 表示フラグ
        """
        return bool(win32gui.IsWindowVisible(self.hwnd))

    def get_filtered_children(self, **kwargs) -> list["Window"]:
        """条件に合致する子ウィンドウを取得する

        Args:
            **kwargs: フィルター条件

        Returns:
            list[WindowObj]: フィルターされた子ウィンドウ一覧
        """
        children = self.children
        for key, value in kwargs.items():
            if not isinstance(value, list):
                value = [value]
            joined_children = []
            for v in value:
                joined_children += [child for child in children if v == getattr(child, key)]
            children = joined_children
        return children

    def get_children_in_hierarchy_on_coordinate(self, x: int, y: int) -> list:
        options = []

        def recursive_callback(hwnd, param):
            rect = win32gui.GetWindowRect(hwnd)
            if rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
                print(f"hit: {hwnd}")
                window = Window(hwnd)
                options.append(window)
                win32gui.EnumChildWindows(hwnd, recursive_callback, 0)
            return True

        win32gui.EnumChildWindows(self.hwnd, recursive_callback, 0)
        return options

    def set_text(self, text: str) -> None:
        """ウィンドウタイトルを設定する

        Args:
            text (str): ウィンドウタイトル
        """
        win32gui.SetWindowText(self.hwnd, text)

    def set_window_position(self, x: int, y: int, w: int, h: int, swp_flags: SWPFlags = SWPFlags.SWP_SHOWWINDOW) -> None:
        """ウィンドウの位置とサイズを設定する

        Args:
            x (int): 左上のx座標
            y (int): 左上のy座標
            w (int): 幅
            h (int): 高さ
        """
        win32gui.SetWindowPos(self.hwnd, 0, x, y, w, h, swp_flags.value)

    def to_top(self) -> None:
        """ウィンドウを最前面に表示する"""
        win32gui.SetForegroundWindow(self.hwnd)

    def hide(self) -> bool:
        """ウィンドウを非表示にする
        
        Returns:
            bool: 以前に表示されていたかどうか
        """
        return bool(win32gui.ShowWindow(self.hwnd, ShowWindowCommands.HIDE.value))

    def show(self) -> bool:
        """ウィンドウを表示する
        
        Returns:
            bool: 以前に表示されていたかどうか
        """
        return bool(win32gui.ShowWindow(self.hwnd, ShowWindowCommands.SHOWNORMAL.value))

    def maximize(self) -> bool:
        """ウィンドウを最大化する"""
        return bool(win32gui.ShowWindow(self.hwnd, ShowWindowCommands.MAXIMIZE.value))

    def minimize(self) -> bool:
        """ウィンドウを最小化する"""
        return bool(win32gui.ShowWindow(self.hwnd, ShowWindowCommands.MINIMIZE.value))

    def activate(self) -> None:
        """ウィンドウをアクティブにする"""
        win32gui.SetForegroundWindow(self.hwnd)

    def set_focus(self) -> None:
        """ウィンドウにフォーカスを当てる"""
        if self.is_active:
            return
        win32gui.SetFocus(self.hwnd)

    def _send_message(
            self,
            act: Win32Constants,
            *,
            word_param: Optional[int] = None,
            long_param: Optional[int] = None
        ) -> int:
        """同期的ウィンドウ操作基底メソッド

        Args:
            act (Win32Constants): win32conメッセージ
            word_param (Optional[int], optional): Defaults to None.
            long_param (Optional[int], optional): Defaults to None.

        Returns:
            int: メッセージの戻り値
        """
        if isinstance(act, Win32Constants):
            act = act.value
        if isinstance(act, str):
            act = int(act, 16)
        return win32gui.SendMessage(self.hwnd, act, word_param, long_param)

    def _post_message(
            self,
            act: Win32Constants,
            *,
            word_param: Optional[int] = None
        ) -> bool:
        """非同期的ウィンドウ操作基底メソッド

        Args:
            act (Win32Constants): win32conメッセージ
            word_param (Optional[int], optional): Defaults to None.
        """
        if isinstance(act, Win32Constants):
            act = act.value
        if isinstance(act, str):
            act = int(act, 16)
        return bool(win32gui.PostMessage(self.hwnd, act, word_param))

    def click(self) -> None:
        """クリックする"""
        self._post_message(Win32Constants.WM_LBUTTONDOWN)
        self._post_message(Win32Constants.WM_LBUTTONUP)

    def send_keys(self, keys: str) -> None:
        """ウィンドウにキー入力を送る

        Args:
            keys (str): キー入力文字列
        """
        self._send_message(Win32Constants.WM_SETTEXT, word_param=0, long_param=keys)

    def close(self) -> None:
        """ウィンドウを閉じる"""
        self._send_message(Win32Constants.WM_CLOSE)

    def _draw_children(self, children: list["Window"], class_colors, colors, ax):
        for child in children:
            # print("==============")
            # print(type(child))
            # pprint(child.get("class_name"))
            # print("==============")
            class_name = child.class_name
            cx1, cy1, cx2, cy2 = child.rect
            hwnd = child.hwnd

            if class_name not in class_colors:
                class_colors[class_name] = next(colors)

            color = class_colors[class_name]
            rect = patches.Rectangle((cx1, cy1), cx2 - cx1, cy2 - cy1, linewidth=1, edgecolor=color, facecolor='none')
            ax.add_patch(rect)
            plt.text((cx1 + cx2) / 2, (cy1 + cy2) / 2, str(hwnd), ha='center', va='center', color=color)
        # raise Exception("Not implemented")

            if len(child.children) > 0:
                self._draw_children(child.children, class_colors, colors, ax)

    def draw_window_obj(self, **kwargs) -> None:
        """子要素とhwnd値の構成を描画する"""
        children = self.get_filtered_children(**kwargs)
        children = [child for child in children]

        class_colors = {}
        colors = iter(plt.cm.tab20.colors)

        fig, ax = plt.subplots()

        x1, y1, x2, y2 = self.rect
        ax.set_xlim(x1, x2)
        ax.set_ylim(y1, y2)

        me_rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(me_rect)
        class_colors['me'] = 'black'

        self._draw_children(children, class_colors, colors, ax)

        plt.gca().invert_yaxis()

        handles = [patches.Patch(color=color, label=class_name) for class_name, color in class_colors.items()]
        plt.legend(handles=handles)

        plt.show()

    def draw_window_obj_tkinter(self, **kwargs) -> None:
        children = self.get_filtered_children(**kwargs)
        children_dict = [child.to_dict() for child in children]

        class_colors = {}
        colors = itertools.cycle(["red", "blue", "green", "purple", "orange"])

        root = tk.Tk()

        x1, y1, x2, y2 = self.rect
        width, height = x2 - x1, y2 - y1
        root.geometry(f"{width}x{height}")

        legend_frame = tk.Frame(root)
        legend_frame.pack(side=tk.TOP, fill=tk.X)

        for child in children_dict:
            cx1, cy1, cx2, cy2 = child['rect']
            hwnd = child['hwnd']
            class_name = child['class_name']

            if class_name not in class_colors:
                class_colors[class_name] = next(colors)

            color = class_colors[class_name]
            button_width = cx2 - cx1
            button_height = cy2 - cy1
            button = tk.Button(root, text=str(hwnd), bg=color, width=button_width, height=button_height)
            button.place(x=cx1 - x1, y=height - (cy2 - y1))

        for class_name, color in class_colors.items():
            label = tk.Label(legend_frame, text=class_name, bg=color, fg="white")
            label.pack(side=tk.LEFT)

        root.mainloop()
