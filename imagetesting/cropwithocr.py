'''
Scanning of menu by cropping and storing in excel file
'''
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image, ImageEnhance

import easyocr
import numpy as np
import openpyxl
import os

class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Uploader")

        self.img_count = 0

        # Editting buttons for cropping
        self.frame_buttons = tk.Frame(self.root, bg='#808080')
        self.frame_buttons.pack(padx=3, pady=3, fill=tk.X)

        self.upload_button = tk.Button(self.frame_buttons, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(padx=3, pady=3, side=tk.LEFT)

        self.crop_button = tk.Button(self.frame_buttons, text='Add Crop', command= self.init_cropping)
        self.crop_button.pack(padx=3, pady=3, side=tk.LEFT)

        self.download_crop_button = tk.Button(self.frame_buttons, text='Download Crop', command= self.save_cropping)
        self.download_crop_button.pack(padx=3, pady=3, side=tk.LEFT)

        self.refresh_btn = tk.Button(self.frame_buttons, text='Refresh', command= self.go_to_original)
        self.refresh_btn.pack(padx=3, pady=3, side=tk.LEFT)

        self.delete_all_btn = tk.Button(self.frame_buttons, text='Delete All', bg= '#DC3545'
                                        , command= self.delete_all_crop)
        self.delete_all_btn.pack(padx=3, pady=3, side=tk.LEFT)


        # Image counting label
        self.saved_img_count = tk.Label(self.frame_buttons, text=f'Saved Images in Directory: {self.img_count}', 
                                        bg='blue', fg='white')
        self.saved_img_count.pack(padx=3,pady=3, side=tk.RIGHT)

        # Canvas for images and cropped images
        self.canvas = tk.Canvas(self.root, width=1200, height=600, bg='#808080')
        self.canvas.pack()

        self.ocr_button = tk.Button(self.frame_buttons, text="Perform OCR", command=self.perform_ocr)
        self.ocr_button.pack(side=tk.LEFT)

        self.reader = easyocr.Reader(['en', 'ch_sim'])  # Initialize EasyOCR reader for English language
        self.start_x = None
        self.start_y = None
        self.rectangle = None
        self.cropped_image = None
        self.crop_mode = False
        self.crop_coords = []

        self.excel_file = None  # Store the Excel file path

        # Ask the user whether to open an existing Excel file or create a new one
        self.open_or_create_excel()

    def open_or_create_excel(self):
        choice = messagebox.askyesno("Excel File", "Do you want to open an existing Excel file?")
        if choice:
            self.open_existing_excel()
        else:
            self.create_new_excel()

    def open_existing_excel(self):
        file_path = filedialog.askopenfilename(title="Open Existing Excel File",
                                            filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.excel_file = file_path

    def create_new_excel(self):
        file_path = filedialog.asksaveasfilename(title="Save As",
                                                 defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.excel_file = file_path

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select Image",
                                            filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")))
        if file_path:
            self.image = Image.open(file_path)
            
            # Resize the image to fit within the specified dimensions
            max_width = 1200
            max_height = 600
            width, height = self.image.size
            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(self.image)

            
            # Update canvas size to match the resized image size
            self.canvas.config(width=self.image.width, height=self.image.height)
            
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def init_cropping(self):
        if self.crop_mode == False:
            self.crop_mode = True

            self.canvas.bind("<ButtonPress-1>", self.start_cropping)
            self.canvas.bind("<B1-Motion>", self.draw_rectangle)
            self.canvas.bind("<ButtonRelease-1>", self.end_cropping)

        elif self.crop_mode == True:
            self.crop_mode = False

            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def start_cropping(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, 
                                                      self.start_y, outline="yellow", width=4)

    def draw_rectangle(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rectangle, self.start_x, self.start_y, cur_x, cur_y)

    def end_cropping(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        
        # Calculate the width and height of the cropped area
        width = end_x - self.start_x
        height = end_y - self.start_y
        
        # Determine the target width and height while maintaining the aspect ratio
        max_width = 800
        max_height = 400

        # Calculate the aspect ratio of the cropped area
        aspect_ratio = width / height

        # Adjust target width and height based on the aspect ratio
        if aspect_ratio > max_width / max_height:
            max_height = int(max_width * aspect_ratio)
        else:
            max_width = int(max_height * aspect_ratio)

        # Check if cropped_image exists
        if self.image:
            # Crop the image
            if self.start_x < end_x and self.start_y < end_y:
                self.coords = [self.start_x, self.start_y, end_x, end_y]
            elif self.start_x > end_x and self.start_y < end_y:
                self.coords = [end_x, self.start_y, self.start_x, end_y]
            elif self.start_x > end_x and self.start_y < end_y:
                self.coords = [end_x, end_y, self.start_x, self.start_y]
            elif self.start_x > end_x and self.start_y < end_y:
                self.coords = [end_x, end_y, self.start_x, self.start_y]

            self.cropped_image = self.image.crop(self.coords)
            print(f'Cropped: {self.coords}')

            # Resize the cropped image while preserving its aspect ratio
            self.canvas.config(width=max_width, height=max_height)
            self.cropped_image = self.cropped_image.resize((max_width, max_height), Image.Resampling.LANCZOS)
            self.cropped_image = self.sharpen_image(self.cropped_image)  # Sharpen the cropped image

            self.cropped_photo = ImageTk.PhotoImage(self.cropped_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_photo)
    
    def sharpen_image(self, image):
        enhancer = ImageEnhance.Sharpness(image)
        sharpened_image = enhancer.enhance(1.5)  # Adjust the enhancement factor as needed
        return sharpened_image
    
    def go_to_original(self):
        self.canvas.delete("all")
        self.canvas.config(width=self.photo.width(), height=self.photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        if self.crop_coords:
            for coord in self.crop_coords:
                self.canvas.create_rectangle(coord[0], coord[1], coord[2], coord[3], 
                                             outline='yellow', width=4)
    
    def delete_all_crop(self):
        # Delete all images saved and crop coords
        self.crop_coords = []
        directory = 'imagetesting/saved_img'
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    print(f"Removed {filepath}")
            except Exception as e:
                print(f"Error while removing {filepath}: {e}")

        self.go_to_original()

    def save_cropping(self):
        # Display img_count
        self.img_count += 1
        self.cropped_image.save(f'imagetesting/saved_img/{self.img_count}.jpg')
        self.saved_img_count.config(text=f'Saved Images in Directory: {self.img_count}')

        self.crop_coords.append(self.coords)

        self.go_to_original()

    def perform_ocr(self):
        if os.listdir('imagetesting/saved_img'):
            for images in os.listdir('imagetesting/saved_img'):
                PIL_image = Image.open(f'imagetesting/saved_img/{images}')

                print('Performing OCR on {}'.format(images))
                
                enhanced_image = ImageEnhance.Contrast(PIL_image).enhance(1.5)

                # Convert the cropped image to a numpy array
                cropped_image_array = np.array(enhanced_image)

                # Perform OCR on the numpy array
                result = self.reader.readtext(cropped_image_array, detail=0)

                if self.excel_file:
                    # Open existing workbook or create new one
                    if os.path.exists(self.excel_file):
                        wb = openpyxl.load_workbook(self.excel_file)
                    else:
                        wb = openpyxl.Workbook()
                        wb.remove(wb.active)  # Remove default sheet

                    ws = wb.create_sheet(f"OCR Results for {images}", 0) if f"OCR Results for {images}" not in wb.sheetnames else wb[f"OCR Results for {images}"]

                    # Find the last row with data
                    last_row = ws.max_row

                    # Write OCR results to Excel starting from the next row
                    for i, text in enumerate(result, start=1):
                        ws.cell(row=last_row + i, column=1, value=text)

                    # Save the workbook
                    wb.save(self.excel_file)
                    print("OCR results appended to", self.excel_file)
                else:
                    print("No Excel file selected.")
            else:
                print("No cropped image available for OCR")

        
def main():

    root = tk.Tk()
    root.config(bg='#000000')
    app = ImageUploaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()