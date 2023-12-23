import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
import os
import numpy as np
from enum import Enum

class ThresholdOp(Enum):
    BINARY = 0
    BINARY_INVERSE = 1
    TRUNCATE = 2
    TO_ZERO = 3
    TO_ZERO_INVERSE = 4

    # cv.THRESH_BINARY
    # cv.THRESH_BINARY_INV
    # cv.THRESH_TRUNC
    # cv.THRESH_TOZERO
    # cv.THRESH_TOZERO_INV


class GlobalThreshold(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Custom Input Dialog")

        self.threshold = tk.IntVar(value=128)
        self.max_val = tk.IntVar(value=255)
        self.thresh_type = ThresholdOp.TO_ZERO
        self.thresh_ops = [value.name for value in ThresholdOp]
        self.otsu = tk.BooleanVar()

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack()

        self.thresh_label = ttk.Label(self.main_frame, text="Select Threshold:")
        self.thresh_label.grid(row=0, column=0, sticky=tk.W)

        self.thresh_slider = ttk.Scale(self.main_frame, from_=0, to=255, orient="horizontal", variable=self.threshold)
        # self.thresh_slider.set(128)
        self.thresh_slider.grid(row=0, column=1, padx=5, pady=5)

        self.max_label = ttk.Label(self.main_frame, text="Select Max Value:")
        self.max_label.grid(row=1, column=0, sticky=tk.W)

        self.max_slider = ttk.Scale(self.main_frame, from_=0, to=255, orient="horizontal", variable=self.max_val)
        # self.max_slider.set(255)
        self.max_slider.grid(row=1, column=1, padx=5, pady=5)

        self.thresh_op_label = ttk.Label(self.main_frame, text="Select mask operation:")
        self.thresh_op_label.grid(row=2, column=0, sticky=tk.W)

        self.thresh_op_dropdown = ttk.Combobox(self.main_frame, values=self.thresh_ops)
        self.thresh_op_dropdown.current(0)
        self.thresh_op_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.otsu_label = ttk.Label(self.main_frame, text="Use Otsu Auto:")
        self.otsu_label.grid(row=3, column=0, sticky=tk.W)

        self.otsu_checkbox = ttk.Checkbutton(self.main_frame, text="Otsu", variable=self.otsu)
        self.otsu_checkbox.grid(row=3, column=1, padx=5, pady=5)

        # OK and Cancel buttons
        self.ok_button = ttk.Button(self.main_frame, text="OK", command=self.on_ok)
        self.ok_button.grid(row=4, column=0, padx=5, pady=10)

        self.cancel_button = ttk.Button(self.main_frame, text="Cancel", command=self.on_cancel)
        self.cancel_button.grid(row=4, column=1, padx=5, pady=10)

    def on_ok(self):
        thresh_op = self.thresh_op_dropdown.get()

        if thresh_op is None:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            self.thresh_op = ThresholdOp[thresh_op]
            self.destroy()

    def on_cancel(self):
        self.destroy()

    def get_values(self):
        return self
   
