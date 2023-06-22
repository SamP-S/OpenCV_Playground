import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import ImageTk, Image
import os
import numpy as np
from enum import Enum

class BitwiseOp(Enum):
    AND = 0
    NOT = 1
    XOR = 2
    
class MaskOp(Enum):
    ADD = 0
    SUB = 1

class CustomInputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Custom Input Dialog")

        self.rgb_lower = np.array([0, 0, 0])
        self.rgb_upper = np.array([128, 128, 128])
        self.bitwise = BitwiseOp.AND
        self.maskop = MaskOp.ADD

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

        # Integer dropdowns
        self.bitwise_label = ttk.Label(self.main_frame, text="Select bitwise operation:")
        self.bitwise_label.grid(row=2, column=0, sticky=tk.W)

        self.bitwise_dropdown = ttk.Combobox(self.main_frame, values=[str(BitwiseOp.AND), str(BitwiseOp.NOT), str(BitwiseOp.XOR)])
        self.bitwise_dropdown.current(0)
        self.bitwise_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.maskop_label = ttk.Label(self.main_frame, text="Select mask operation:")
        self.maskop_label.grid(row=3, column=0, sticky=tk.W)

        self.maskop_dropdown = ttk.Combobox(self.main_frame, values=[str(MaskOp.ADD), str(MaskOp.SUB)])
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
        bitwise = self.bitwise_dropdown.get()
        maskop = self.maskop_dropdown.get()

        if self.rgb_lower is None or self.rgb_upper is None or bitwise is None or maskop is None:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            self.bitwise = bitwise
            self.maskop = maskop
            self.destroy()

    def on_cancel(self):
        self.destroy()

    def get_values(self):
        return self
   

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor")
        self.image_stack = []
        self.stack_index = -1
        self.initial_dir = os.getenv("HOME") + "/nfs/1914-1926/Bowling_Harbour_1914/"
        self.default_image_path = self.initial_dir + "1914_007.tif"
        self.filepath = self.default_image_path
        self.image_width = 1280
        self.image_height = 720

        # Create UI elements
        self.create_menu()
        self.create_side_panel()
        self.create_image_display()
        self.create_navigation_buttons()
        self.load_image()

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def create_image_display(self):
        self.image_display = tk.Canvas(self, width=1280, height=720)
        self.image_display.pack()
        self.image_label = tk.Label(self)
        self.image_label.pack()   

    def create_side_panel(self):
        panel_frame = tk.Frame(self)
        panel_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.panel_buttons = []
        functions = [("Grayscale", self.apply_grayscale),
                     ("Blur", self.apply_blur),
                     ("Canny Edge", self.apply_canny_edge),
                     ("Colour Filter", self.apply_colour_filter)]

        for label, func in functions:
            button = tk.Button(panel_frame, text=label, width=15, command=func)
            button.pack(side=tk.TOP, pady=5)
            self.panel_buttons.append(button)

    def create_navigation_buttons(self):
        self.nav_frame = tk.Frame(self)
        self.nav_frame.pack(side=tk.BOTTOM, pady=10)

        self.back_button = tk.Button(self.nav_frame, text="Back", width=10, command=self.undo_operation)
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        self.nav_label = tk.Label(self, text="0")
        self.nav_label.pack() 

        self.forward_button = tk.Button(self.nav_frame, text="Forward", width=10, command=self.redo_operation)
        self.forward_button.pack(side=tk.LEFT, padx=5)

    def open_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("TIF Files", "*.tif")], initialdir=self.initial_dir)
        if filepath:
            print(filepath)
            self.filepath = filepath
            self.load_image()

    def load_image(self, event=None):
        image = cv2.imread(self.filepath)
        if image is not None:
            self.push_img_stack(image)
            self.display_image()
        else:
            messagebox.showerror("Error", "Failed to load image.")

    def display_image(self, event=None):
        pil_image = Image.fromarray(cv2.cvtColor(self.current_image(), cv2.COLOR_BGR2RGB))
        pil_image = pil_image.resize((self.image_width, self.image_height))
        self.tk_photo = ImageTk.PhotoImage(pil_image)
        self.image_display.create_image(0, 0, anchor=tk.NW, image=self.tk_photo)
        self.image_display.pack()
        self.image_label.configure(text=self.filepath)
        self.image_label.pack()
        self.nav_label.configure(text=str(self.stack_index) + "/" + str(len(self.image_stack) - 1))
        self.nav_label.pack() 
    
    def current_image(self):
        return self.image_stack[self.stack_index]

    def apply_grayscale(self):
        if self.current_image() is not None:
            gray_image = cv2.cvtColor(self.current_image(), cv2.COLOR_BGR2GRAY)
            self.push_img_stack(gray_image)
            self.display_image()

    def apply_blur(self):
        if self.current_image() is not None:
            blurred_image = cv2.blur(self.current_image(), (5, 5))
            self.push_img_stack(blurred_image)
            self.display_image()
    
    def apply_canny_edge(self):
        return
    
    def apply_colour_filter(self):
        dialog = CustomInputDialog(self)
        dialog.wait_window()
    
        if dialog.rgb_lower is not None and dialog.rgb_upper is not None and dialog.bitwise is not None and dialog.maskop is not None:
            print("Lower (RGB):", dialog.rgb_lower)
            print("Higher (RGB):", dialog.rgb_upper)
            print("Bitwise Operation:", dialog.bitwise)
            print("Mask Operation:", dialog.maskop)
        else:
            print("Dialog canceled.")
            
        if self.current_image() is not None:
            filter_mask = cv2.inRange(self.current_image(), dialog.rgb_lower, dialog.rgb_upper)
            if (dialog.bitwise == BitwiseOp.AND):
                masked_image = cv2.bitwise_and(self.current_image(), self.current_image(), mask=filter_mask)
            elif (dialog.bitwise == BitwiseOp.NOT):
                masked_image = cv2.bitwise_not(self.current_image(), self.current_image(), mask=filter_mask)
            else:
                masked_image = cv2.bitwise_xor(self.current_image(), self.current_image(), mask=filter_mask)

            if (dialog.maskop == MaskOp.ADD):
                result = self.current_image() + masked_image
            else:
                result = self.current_image() - masked_image

            
            # push all filter stages
            self.push_img_stack(filter_mask)
            self.push_img_stack(masked_image)
            self.push_img_stack(result)
            self.display_image()
    
    
    def push_img_stack(self, img):
        if (img is None):
            return
        self.image_stack = self.image_stack[:self.stack_index + 1]
        self.image_stack.append(img)
        self.stack_index = len(self.image_stack) - 1
    
    def undo_operation(self):
        self.stack_index -= 1
        if (self.stack_index <= 0):
            self.stack_index = 0
        self.display_image()
    
    def redo_operation(self):
        self.stack_index += 1
        if (self.stack_index >= len(self.image_stack)):
            self.stack_index = len(self.image_stack) - 1
        self.display_image()

app = ImageEditor()
app.mainloop()