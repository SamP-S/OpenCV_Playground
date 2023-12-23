import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
import os
import numpy as np
from enum import Enum

class ColourFilter(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Custom Input Dialog")

        self.red = tk.BooleanVar()
        self.green = tk.BooleanVar()
        self.blue = tk.BooleanVar()

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack()

        # Color pickers
        self.red_label = ttk.Label(self.main_frame, text="Filter Red:")
        self.red_label.grid(row=0, column=0, sticky=tk.W)

        self.red_checkbox = ttk.Checkbutton(self.main_frame, text="Red", variable=self.red)
        self.red_checkbox.grid(row=0, column=1, padx=5, pady=5)

        self.green_label = ttk.Label(self.main_frame, text="Filter Green:")
        self.green_label.grid(row=1, column=0, sticky=tk.W)

        self.green_checkbox = ttk.Checkbutton(self.main_frame, text="Green", variable=self.green)
        self.green_checkbox.grid(row=1, column=1, padx=5, pady=5)

        self.blue_label = ttk.Label(self.main_frame, text="Filter Blue:")
        self.blue_label.grid(row=2, column=0, sticky=tk.W)

        self.blue_checkbox = ttk.Checkbutton(self.main_frame, text="Blue", variable=self.blue)
        self.blue_checkbox.grid(row=2, column=1, padx=5, pady=5)

        # OK and Cancel buttons
        self.ok_button = ttk.Button(self.main_frame, text="OK", command=self.on_ok)
        self.ok_button.grid(row=4, column=0, padx=5, pady=10)

        self.cancel_button = ttk.Button(self.main_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=4, column=1, padx=5, pady=10)

    def on_ok(self):
        self.destroy()

    def on_cancel(self):
        self.destroy()

    def get_values(self):
        return self
   
