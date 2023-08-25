import tkinter as tk
from tkinter import ttk
import win32gui
from modules.window import Window
from modules.desktop import Desktop
from fire import Fire
from PIL import Image, ImageTk


class WindowPicker(tk.Tk):
    def __init__(self, width: int = 450, height: int = 400, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.desktop = Desktop()
        self.title("Window Picker")
        self.geometry(f"{width}x{height}")
        self.selected_handle = tk.StringVar()
        canvas_width, canvas_height = 80, 60
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        pil_image = Image.open("target.png")
        pil_image = pil_image.convert("RGBA")
        self.image = ImageTk.PhotoImage(image=pil_image)

        image_id = self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.image)
        self.canvas.tag_bind(image_id, "<Button-1>", self._start_drag)
        self.canvas.tag_bind(image_id, "<B1-Motion>", self._on_drag)
        self.canvas.tag_bind(image_id, "<ButtonRelease-1>", self._on_drop)

        self.drag_window = tk.Toplevel(self)
        self.drag_window.overrideredirect(1)
        self.drag_window.geometry("32x32")
        drag_window_label = tk.Label(self.drag_window, image=self.image)
        drag_window_label.pack()
        self.drag_window.withdraw()

        self.dropdown_menu = tk.OptionMenu(self, self.selected_handle, "")
        self.dropdown_menu.pack()

        self.selected_handle.trace("w", self._on_handle_selected)

        self.info_table = ttk.Treeview(self, columns=("Property", "Value"), show="headings")
        self.info_table.heading("Property", text="Property")
        self.info_table.heading("Value", text="Value")
        self.info_table.pack()

    def _get_handles_in_hierarchy(self, hwnd, x, y):
        options = []
        
        def recursive_callback(handle, level):
            rect = win32gui.GetWindowRect(handle)
            if rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
                window_text = win32gui.GetWindowText(handle)
                indent = " " * level * 4
                option = f"{indent}Handle: {handle}, Title: {window_text}"
                options.append(option)
                win32gui.EnumChildWindows(handle, recursive_callback, level + 1)

        win32gui.EnumChildWindows(hwnd, recursive_callback, 0)
        return options

    def _on_drop(self, event):
        self.drag_window.withdraw()
        x, y = self.winfo_pointerx(), self.winfo_pointery()

        options = []
        for window in self.desktop.get_all_top_visibile_windows():
            rect = window.rect
            if rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
                options.append(window)
                options.extend(window.get_children_in_hierarchy_on_coordinate(x, y))

        self.dropdown_menu['menu'].delete(0, 'end')
        self.selected_handle.set(options[0] if options else "")
        for option in options:
            self.dropdown_menu['menu'].add_command(label=option, command=tk._setit(self.selected_handle, option))

    def _on_handle_selected(self, *args):
        print(self.selected_handle.get())
        selected_option = self.selected_handle.get()
        handle_str = selected_option.split(" ")[0].replace("[", "").replace("]", "")
        handle = int(handle_str)
        selected_obj = Window(handle)
        window_info_dict = selected_obj.to_dict()

        for row in self.info_table.get_children():
            self.info_table.delete(row)

        for key, value in window_info_dict.items():
            self.info_table.insert("", tk.END, values=(key, value))

    def _start_drag(self, event):
        self.drag_window.deiconify()

    def _on_drag(self, event):
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        self.drag_window.geometry(f"+{x-16}+{y-16}")


def main(w: int = 450, h:int = 400):
    app = WindowPicker(width=w, height=h)
    app.mainloop()


if __name__ == "__main__":
    Fire(main)