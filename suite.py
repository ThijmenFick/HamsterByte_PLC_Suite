import threading

from PIL import Image
import dearpygui.dearpygui as dpg
import numpy as np
import tkinter as tk
from tkinter import filedialog

dpg.create_context()
root = tk.Tk()
root.withdraw()


def load_texture(path, size=(32, 32)):
    img = Image.open(path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)  # force correct size
    data = np.frombuffer(img.tobytes(), dtype=np.uint8) / 255.0  # normalize to [0,1]
    return data.tolist()

alert_image_data = load_texture("windows_xp/alert.png")
error_image_data = load_texture("windows_xp/error.png")
info_image_data = load_texture("windows_xp/info.png")
no_pc_image_data = load_texture("windows_xp/no_pc.png")

with dpg.texture_registry(show=False):
    dpg.add_static_texture(32, 32, alert_image_data, tag="alert_icon")
    dpg.add_static_texture(32, 32, error_image_data, tag="error_icon")
    dpg.add_static_texture(32, 32, info_image_data, tag="info_icon")
    dpg.add_static_texture(32, 32, no_pc_image_data, tag="no_pc_icon")

def show_alert(type, title, content):
    with dpg.window(label=title, modal=True, no_close=True, tag="msg_window"):
        dpg.add_image(type)  # show icon
        dpg.add_text(content)
        dpg.add_button(label="OK", width=75,
                       callback=lambda s, a: dpg.delete_item("msg_window"))

def callback(sender, app_data):
    print(app_data["file_path_name"])


with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=700 ,height=400):
    dpg.add_file_extension("PLC Projects (*.plcp){.plcp}", color=(0, 255, 255, 255))


with dpg.window(label="Main Window", tag="main_window",
                pos=[0, 0],
                no_move=True, no_close=True, no_collapse=True):

    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="New Project", callback=lambda : print("New"))
            dpg.add_menu_item(label="Open Project", callback=lambda: dpg.show_item("file_dialog_id"))
            dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())

        with dpg.menu(label="Edit"):
            dpg.add_menu_item(label="Undo", callback=lambda: print("Undo"))
            dpg.add_menu_item(label="Redo", callback=lambda: print("Redo"))

        with dpg.menu(label="About"):
            dpg.add_menu_item(label="Info", callback=lambda: show_alert("info_icon", "About", "HamsterByte PLC Suite is the official software to work with the HamsterBytes PLC line"))


    with dpg.group(horizontal=True):

        with dpg.child_window(tag="left_window", width=250, autosize_y=True, border=True):
            dpg.add_text("Project Tree")
            dpg.add_text("Main.st")
            dpg.add_text("Main.ld")


        with dpg.child_window(tag="right_window", autosize_x=True, autosize_y=True, border=True):
            dpg.add_text("Editor Area")


# Auto-resize main window to viewport
def resize_main_window(sender, app_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.configure_item("main_window", width=width, height=height)


dpg.set_viewport_resize_callback(resize_main_window)

dpg.create_viewport(title='PLC Suite', width=900, height=600)
resize_main_window(None, None)  # initialize size before showing
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
