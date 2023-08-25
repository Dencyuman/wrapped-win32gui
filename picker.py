import tkinter as tk
from tkinter import ttk
import win32gui

from modules.window import Window

def enum_child_windows(hwnd, drop_x, drop_y):
    result = []

    def callback(handle, param):
        rect = win32gui.GetWindowRect(handle)
        if rect[0] <= drop_x <= rect[2] and rect[1] <= drop_y <= rect[3]:
            result.append(handle)
        return True

    win32gui.EnumChildWindows(hwnd, callback, None)
    return result

def get_window_handle(x, y):
    handle = win32gui.WindowFromPoint((x, y))
    while win32gui.GetParent(handle) != 0:
        handle = win32gui.GetParent(handle)
    return handle

def on_drop(event):
    drag_window.withdraw()  # 透過ウィンドウを消す
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    handle = get_window_handle(x, y)
    top_level_window_handle = handle
    top_window_text = win32gui.GetWindowText(handle)
    top_option = f"Top Level Handle: {handle}, Title: {top_window_text}"

    child_handles = enum_child_windows(top_level_window_handle, x, y)
    options = [top_option]
    for handle in child_handles:
        window_text = win32gui.GetWindowText(handle)
        option = f"Handle: {handle}, Title: {window_text}"
        options.append(option)

    # 既存のオプションを更新
    dropdown_menu['menu'].delete(0, 'end')
    selected_handle.set(options[0])
    for option in options:
        dropdown_menu['menu'].add_command(label=option, command=tk._setit(selected_handle, option))


def on_handle_selected(*args):
    print(selected_handle.get())
    selected_option = selected_handle.get()
    handle_str = selected_option.split(",")[0].split(":")[1].strip()
    handle = int(handle_str)
    selected_obj = Window(handle)
    window_info_dict = selected_obj.to_dict()

    # テーブルの内容をクリア
    for row in info_table.get_children():
        info_table.delete(row)

    # 新しい情報をテーブルに追加
    for key, value in window_info_dict.items():
        info_table.insert("", tk.END, values=(key, value))

def start_drag(event):
    drag_window.deiconify()

def on_drag(event):
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    drag_window.geometry(f'+{x-16}+{y-16}')

root = tk.Tk()
root.title('Window Picker')
root.geometry('400x300')
selected_handle = tk.StringVar()
canvas_width, canvas_height = 80, 60
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

image_path = './assets/target.png'
image = tk.PhotoImage(file=image_path)

image_id = canvas.create_image(canvas_width // 2, canvas_height // 2, image=image)
canvas.tag_bind(image_id, '<Button-1>', start_drag)
canvas.tag_bind(image_id, '<B1-Motion>', on_drag)
canvas.tag_bind(image_id, '<ButtonRelease-1>', on_drop)

drag_window = tk.Toplevel(root)
drag_window.overrideredirect(1)
drag_window.geometry('32x32')
drag_window_label = tk.Label(drag_window, image=image)
drag_window_label.pack()
drag_window.withdraw()

# ウィンドウ情報を表示するラベルのリスト
info_labels = []

# 初期のドロップダウンメニュー
dropdown_menu = tk.OptionMenu(root, selected_handle, "")
dropdown_menu.pack()

# ドロップダウンメニューからの選択を処理
selected_handle.trace('w', on_handle_selected)

# ウィンドウ情報を表示するテーブル
info_table = ttk.Treeview(root, columns=("Property", "Value"), show="headings")
info_table.heading("Property", text="Property")
info_table.heading("Value", text="Value")
info_table.pack()

root.mainloop()