import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import ImageTk, Image
import os
import numpy as np
from enum import Enum
from colour_mask import *
from colour_filter import *
from global_threshold import *

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor")
        self.image_stack = []
        self.stack_index = -1
        self.initial_dir = os.getcwd()
        self.filepath = None
        self.image_width = 1280
        self.image_height = 720

        # Create UI elements
        self.create_menu()
        self.create_side_panel()
        self.create_image_display()
        self.create_navigation_buttons()

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
        functions = [  
                        ("Grayscale", self.apply_grayscale),
                        ("Blur", self.apply_blur),
                        ("Sharpen", self.apply_sharpen),
                        ("Global Threshold", self.apply_global_threshold),  
                        ("Canny Edge", self.apply_canny_edge),
                        ("Colour Mask", self.apply_colour_mask),
                        ("Colour Filter", self.apply_colour_filter),
                        ("Contrast", self.apply_contrast),
                        ("Rescale", self.apply_rescale)
                    ]

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
        filepath = filedialog.askopenfilename(filetypes=[("All Files", "*.*")], initialdir=self.initial_dir)
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

    def apply_sharpen(self):
        if self.current_image() is not None:
            copy_img = self.current_image().copy()
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            copy_img = cv2.filter2D(copy_img, -1, kernel)  
            self.push_img_stack(copy_img)
            self.display_image()  
    
    def apply_canny_edge(self):
        return

    def apply_contrast(self):
        if self.current_image() is not None:
            copy_image = self.current_image().copy()
            array_alpha = np.array([1.5])
            array_beta = np.array([-50.0])

            contrast_img = cv2.add(copy_image, array_beta)                    

            new_img = cv2.multiply(contrast_img, array_alpha)  
            self.push_img_stack(new_img)
            self.display_image()

    def apply_colour_filter(self):
        if self.current_image() is not None:
            dialog = ColourFilter(self)
            dialog.wait_window()

            colour_base = self.current_image().copy()
            if dialog.red.get():
                colour_base[:, :, 2] = 0
            if dialog.green.get():
                colour_base[:, :, 1] = 0
            if dialog.blue.get():
                colour_base[:, :, 0] = 0

            self.push_img_stack(colour_base)
            self.display_image()
    
    def apply_colour_mask(self):
        dialog = ColourMask(self)
        dialog.wait_window()
    
        if dialog.rgb_lower is not None and dialog.rgb_upper is not None and dialog.maskop is not None:
            print("Lower (RGB):", dialog.rgb_lower)
            print("Higher (RGB):", dialog.rgb_upper)
            print("Mask Operation:", dialog.maskop)
        else:
            print("Dialog canceled.")
            
        if self.current_image() is not None:
            copy_img = self.current_image().copy()
            filter_mask = cv2.inRange(copy_img, dialog.rgb_lower, dialog.rgb_upper)
            print("op:", dialog.maskop)
            result_image = None
            masked_image = cv2.bitwise_and(copy_img, copy_img, mask=filter_mask)
            if (dialog.maskop.value == MaskOp.ADD.value):
                result_image = self.current_image() + masked_image
            elif (dialog.maskop.value == MaskOp.SUB.value):
                result_image = self.current_image() - masked_image
            elif (dialog.maskop.value == MaskOp.AND.value):
                result_image = masked_image
            elif (dialog.maskop.value == MaskOp.NOT.value):
                result_image = cv2.bitwise_not(self.current_image(), self.current_image(), mask=filter_mask)
            elif (dialog.maskop.value == MaskOp.XOR.value):
                result_image = cv2.bitwise_xor(self.current_image(), self.current_image(), mask=filter_mask)
            elif (dialog.maskop.value == MaskOp.OR.value):
                result_image = cv2.bitwise_xor(self.current_image(), self.current_image(), mask=filter_mask)
            else:
                print("huh")
            # push all filter stages
            self.push_img_stack(filter_mask)
            if result_image is not None:
                self.push_img_stack(result_image)
            self.display_image()
    
    def apply_global_threshold(self):
        if self.current_image() is not None:
            dialog = GlobalThreshold(self)
            dialog.wait_window()

            copy_img = self.current_image().copy()
            thresh = dialog.threshold.get()
            max_val = dialog.max_val.get()
            if (dialog.thresh_op.value == ThresholdOp.BINARY.value):
                thresh_op = cv2.THRESH_BINARY
            elif (dialog.thresh_op.value == ThresholdOp.BINARY_INVERSE.value):
                thresh_op = cv2.THRESH_BINARY_INV
            elif (dialog.thresh_op.value == ThresholdOp.TRUNCATE.value):
                thresh_op = cv2.THRESH_TRUNC
            elif (dialog.thresh_op.value == ThresholdOp.TO_ZERO.value):
                thresh_op = cv2.THRESH_TOZERO
            else: 
                thresh_op = cv2.THRESH_TOZERO_INV
            
            if dialog.otsu.get():
                thresh_op += cv2.THRESH_OTSU   
            used_thresh,thresh_img = cv2.threshold(copy_img, thresh, max_val, thresh_op) 
            self.push_img_stack(thresh_img)
            self.display_image()
            
    # def rescale_nearest(self, array, scale_factor):
    #     # Compute the new shape based on the scale factor
    #     new_shape = np.array(array.shape) * scale_factor

    #     # Use np.kron() to repeat the elements and create the rescaled array
    #     rescaled_array = np.kron(array, np.ones(scale_factor)).reshape(new_shape)

    #     return rescaled_array

    def apply_rescale(self):
        if self.current_image() is not None:
            copy_img = self.current_image().copy()
            for y,row in enumerate(copy_img):
                for x,value in enumerate(row):
                    pass
        # new_img = self.rescale_nearest(copy_img, 0.5)
        # print(new_img.shape)

                        
    
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
