import threading
import zipfile
import tempfile
from PIL import Image
import dearpygui.dearpygui as dpg
import numpy as np
import tkinter as tk
import os

dpg.create_context()
root = tk.Tk()
root.withdraw()

temp_dir_obj = tempfile.TemporaryDirectory(prefix="HamsterByteProject_")
temp_dir = temp_dir_obj.name
print(f"Using temporary directory: {temp_dir}")
active_file = ""


#======== icon initialize for message boxes ========#
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

def open_file_in_editor(file, root):
    global active_file
    active_file = file
    print(active_file)
    if file.endswith(".st"):
        with open(os.path.join(root, file), "r") as file:
            single_line_string = file.read()

        dpg.configure_item(editor, readonly=False, default_value=single_line_string)

#======== Object for file dialog for .plcp files for open project ========#
def callback(sender, app_data):
    print(f"Loaded project from {app_data["file_path_name"]}")
    with zipfile.ZipFile(app_data["file_path_name"], 'r') as zf:
        zf.extractall(temp_dir)
    dpg.set_value("project_name", f"Current: {app_data["file_name"]}")
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            dpg.add_button(label=file, callback=lambda s, a, u: open_file_in_editor(u, root), user_data=file, parent="left_window", tag=file)
            print(file)
    show_alert("info_icon", "Loaded PLCP", f"Loaded PLC-Project {app_data["file_name"]}")

with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=700 ,height=400):
    dpg.add_file_extension("PLC Projects (*.plcp){.plcp}", color=(0, 255, 255, 255))

#======== Detect file change and add * to filename ========#
def on_text_change(sender, app_data, user_data):
    print(f"Current text: {app_data}")
    dpg.configure_item(active_file, label=f"{active_file}*")

#======== Main GUI window ========#
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
            dpg.add_text("No PLC Project opened!", tag="project_name")

        with dpg.child_window(tag="right_window", autosize_x=True, autosize_y=True, border=True):
            editor = dpg.add_input_text(
                default_value="This is initially read-only",
                multiline=True,
                width=-1,
                height=-1,
                readonly=True,
                callback=on_text_change
            )

def resize_main_window(sender, app_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.configure_item("main_window", width=width, height=height)


dpg.set_viewport_resize_callback(resize_main_window)
dpg.create_viewport(title='PLC Suite', width=900, height=600)
resize_main_window(None, None)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
