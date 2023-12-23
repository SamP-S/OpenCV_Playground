import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
import os
import numpy as np
from enum import Enum

class MaskOp(Enum):
    ADD = 0
    SUB = 1
    AND = 2
    NOT = 3
    XOR = 4
    OR = 5

class ColourMask(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Custom Input Dialog")

        self.rgb_lower = np.array([0, 0, 0])
        self.rgb_upper = np.array([128, 128, 128])
        self.maskop = MaskOp.ADD
        self.maskops = [value.name for value in MaskOp]

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack()

        # Color pickers
        self.color1_label = ttk.Label(self.main_frame, text="Select Lower Colour:")
        self.color1_label.grid(row=0, column=0, sticky=tk.W)

        self.color1_button = ttk.Button(self.main_frame, text="Choose RGB", command=self.choose_color1)
        self.color1_button.grid(row=0, column=1, padx=5, pady=5)

        self.color2_label = ttk.Label(self.main_frame, text="Select Upper Colour:")
        self.color2_label.grid(row=1, column=0, sticky=tk.W)

        self.color2_button = ttk.Button(self.main_frame, text="Choose RGB", command=self.choose_color2)
        self.color2_button.grid(row=1, column=1, padx=5, pady=5)

        self.maskop_label = ttk.Label(self.main_frame, text="Select mask operation:")
        self.maskop_label.grid(row=3, column=0, sticky=tk.W)

        self.maskop_dropdown = ttk.Combobox(self.main_frame, values=self.maskops)
        self.maskop_dropdown.current(0)
        self.maskop_dropdown.grid(row=3, column=1, padx=5, pady=5)

        # OK and Cancel buttons
        self.ok_button = ttk.Button(self.main_frame, text="OK", command=self.on_ok)
        self.ok_button.grid(row=4, column=0, padx=5, pady=10)

        self.cancel_button = ttk.Button(self.main_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=4, column=1, padx=5, pady=10)

    def choose_color1(self):
        color = tk.colorchooser.askcolor()
        if color[0] is not None:
            self.rgb_lower = np.array(color[0][:3])

    def choose_color2(self):
        color = tk.colorchooser.askcolor()
        if color[0] is not None:
            self.rgb_upper = np.array(color[0][:3])

    def on_ok(self):
        maskop = self.maskop_dropdown.get()

        if self.rgb_lower is None or self.rgb_upper is None or maskop is None:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            self.maskop = MaskOp[maskop]
            self.destroy()

    def on_cancel(self):
        self.destroy()

    def get_values(self):
        return self
   
