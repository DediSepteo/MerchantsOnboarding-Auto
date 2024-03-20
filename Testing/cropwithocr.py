import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import easyocr
import numpy as np

class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Uploader")

        self.canvas = tk.Canvas(self.root, width=1200, height=900)
        self.canvas.pack()

        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.ocr_button = tk.Button(self.root, text="Perform OCR", command=self.perform_ocr)
        self.ocr_button.pack()

        self.reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader for English language
        self.start_x = None
        self.start_y = None
        self.rectangle = None
        self.cropped_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select Image",
                                               filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")))
        if file_path:
            self.image = Image.open(file_path)
            #self.image = self.image.resize((1280, 900))
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.bind("<ButtonPress-1>", self.start_cropping)
            self.canvas.bind("<B1-Motion>", self.draw_rectangle)
            self.canvas.bind("<ButtonRelease-1>", self.end_cropping)

    def start_cropping(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def draw_rectangle(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rectangle, self.start_x, self.start_y, cur_x, cur_y)

    def end_cropping(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        self.cropped_image = self.image.crop((self.start_x, self.start_y, end_x, end_y))
        self.cropped_photo = ImageTk.PhotoImage(self.cropped_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.cropped_photo)

    def perform_ocr(self):
        if self.cropped_image:
            resized_image = self.cropped_image.resize((1200, 800))

            # Convert the cropped image to a numpy array
            cropped_image_array = np.array(resized_image)

            # Perform OCR on the numpy array
            result = self.reader.readtext(cropped_image_array, detail = 0)

            print(result)  # You can display or process the OCR result as needed
        else:
            print("No cropped image available for OCR")
    
def main():
    root = tk.Tk()
    app = ImageUploaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
