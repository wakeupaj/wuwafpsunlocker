import sys
import os
import sqlite3
import json
from tkinter import Tk, Button, messagebox, filedialog, ttk
from pathlib import Path
import sv_ttk

def update_fps_to_max(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Value FROM LocalStorage WHERE Key = 'GameQualitySetting'")
        current_settings_json = cursor.fetchone()[0]
        current_settings = json.loads(current_settings_json)
        current_settings['KeyCustomFrameRate'] = 120  # Set FPS to the maximum valid value
        updated_settings_json = json.dumps(current_settings)
        cursor.execute("UPDATE LocalStorage SET Value = ? WHERE Key = 'GameQualitySetting'", (updated_settings_json,))
        conn.commit()
        messagebox.showinfo("Success", "FPS set to maximum successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def select_directory():
    directory = filedialog.askdirectory(title='Select the "Wuthering Waves Game" folder')
    if directory:
        # Assuming the .db file is located in 'Client/Saved/LocalStorage/LocalStorage.db' relative to the game folder
        db_path = Path(directory) / "Client" / "Saved" / "LocalStorage" / "LocalStorage.db"
        if db_path.is_file():
            return str(db_path)
        else:
            messagebox.showerror("Error", "The LocalStorage.db file was not found in the selected directory.\n\nMake sure you're selecting the folder titled:\n\"Wuthering Waves Game\"")
            return None
    return None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def setup_theme(root):
    theme_path = resource_path("sv_ttk\dark.tcl")  # Folder where your theme files are stored
    root.tk.call("source", os.path.join(theme_path, "sun-valley.tcl"))
    root.tk.call("set_theme", "dark") 

def create_gui():
    root = Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (350 / 2)
    y = (screen_height / 2) - (250 / 2)
    root.geometry(f"350x250+{int(x)}+{int(y)}")

    root.title("WuWa FPS Unlocker")
    root.geometry("350x250")
    root.iconbitmap(resource_path("wuwafulogo.ico"))
    root.resizable(False, False)

    sv_ttk.set_theme("dark")

    # Variable to hold the path to the DB
    db_path = [None]  # Use a mutable container to hold the path

    btn_select = ttk.Button(root, text="Select Folder", command=lambda: update_db_path())
    btn_select.pack(pady=30)

    # Button to set FPS to 120
    btn_set_fps = ttk.Button(root, text="Unlock FPS", state="disabled", command=lambda: update_fps_to_max(db_path[0]))
    btn_set_fps.pack(pady=25)

    def update_db_path():
        selected_path = select_directory()
        if selected_path:
            db_path[0] = selected_path
            btn_set_fps.config(state="normal")
        else:
            btn_set_fps.config(state="disabled")

    if hasattr(sys, '_MEIPASS'):
        # Import only when run by PyInstaller
        import pyi_splash
        pyi_splash.close()    

    root.mainloop()

if __name__ == "__main__":
    create_gui()