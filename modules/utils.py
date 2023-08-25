from enum import Enum

import win32con


class SWPFlags(Enum):
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_NOZORDER = 0x0004
    SWP_NOREDRAW = 0x0008
    SWP_NOACTIVATE = 0x0010
    SWP_FRAMECHANGED = 0x0020
    SWP_SHOWWINDOW = 0x0040
    SWP_HIDEWINDOW = 0x0080
    SWP_NOCOPYBITS = 0x0100
    SWP_NOOWNERZORDER = 0x0200
    SWP_NOSENDCHANGING = 0x0400



class ShowWindowCommands(Enum):
    """### ShowWindow関数のnCmdShowの値を表すEnumクラス。

    Values:
        - HIDE: ウィンドウを非表示にします。
        - SHOWNORMAL: ウィンドウを通常の位置、サイズで表示します。
        - MINIMIZED: ウィンドウを最小化してアクティブにします。
        - MAXIMIZE: ウィンドウを最大化してアクティブにします。
        - SHOWNOACTIVATE: ウィンドウを通常の位置、サイズで表示しますが、アクティブにはしません。
        - SHOW: ウィンドウを現在のサイズ、位置で表示します。
        - MINIMIZE: ウィンドウを最小化します。
        - SHOWMINNOACTIVE: ウィンドウを最小化しますが、アクティブにはしません。
        - SHOWNA: ウィンドウを現在の状態で表示しますが、アクティブにはしません。
        - RESTORE: ウィンドウをアクティブにして表示します。最小化または最大化されている場合、元のサイズと位置に戻します。
        - SHOWDEFAULT: 起動時に指定されたSWフラグに基づいて表示状態を設定します。
    """
    
    HIDE = 0
    """ウィンドウを非表示にします。"""
    
    SHOWNORMAL = 1
    """ウィンドウを通常の位置、サイズで表示します。"""
    
    MINIMIZED = 2
    """ウィンドウを最小化してアクティブにします。"""
    
    MAXIMIZE = 3
    """ウィンドウを最大化してアクティブにします。"""
    
    SHOWNOACTIVATE = 4
    """ウィンドウを通常の位置、サイズで表示しますが、アクティブにはしません。"""
    
    SHOW = 5
    """ウィンドウを現在のサイズ、位置で表示します。"""
    
    MINIMIZE = 6
    """ウィンドウを最小化します。"""
    
    SHOWMINNOACTIVE = 7
    """ウィンドウを最小化しますが、アクティブにはしません。"""
    
    SHOWNA = 8
    """ウィンドウを現在の状態で表示しますが、アクティブにはしません。"""
    
    RESTORE = 9
    """ウィンドウをアクティブにして表示します。最小化または最大化されている場合、元のサイズと位置に戻します。"""
    
    SHOWDEFAULT = 10
    """起動時に指定されたSWフラグに基づいて表示状態を設定します。"""


def _get_win32con_constants():
    """win32conモジュールの定数を取得する

    Returns:
        dict[str, int]: 定数名と値の辞書
    """
    constants = {}
    for attr in dir(win32con):
        if attr.isupper():
            value = getattr(win32con, attr)
            constants[attr] = value
    return constants

Win32Constants = Enum('Win32Constants', _get_win32con_constants())