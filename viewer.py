import time
from modules.desktop import Desktop


desktop = Desktop()
time.sleep(0.5)

title_keyword = "" # ここにウィンドウのタイトルを入力

apps = desktop.get_windows_by_name(str(title_keyword))
app = apps[0]
app.set_window_position(x=0, y=0, w=800, h=600)
app.draw_window_obj()