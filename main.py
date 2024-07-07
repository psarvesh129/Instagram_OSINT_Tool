import tkinter as tk
from tkinter import ttk
from ui_components import create_login_widgets, create_profile_widgets, create_actions_widgets
from helpers import run_with_proxychains, get_random_user_agent

class InstagramOSINTTool2024:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram OSINT Tool 2024")
        self.root.geometry("1200x800")

        self.profile = None  
        self.L = None  

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.login_frame = ttk.Frame(notebook)
        self.profile_frame = ttk.Frame(notebook)
        self.actions_frame = ttk.Frame(notebook)

        notebook.add(self.login_frame, text="Login")
        notebook.add(self.profile_frame, text="Profile Info")
        notebook.add(self.actions_frame, text="Actions")

        create_login_widgets(self, self.login_frame)
        create_profile_widgets(self, self.profile_frame)
        create_actions_widgets(self, self.actions_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramOSINTTool2024(root)
    root.mainloop()

# GPCSSI2024CW407
