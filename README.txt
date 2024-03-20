# Image Uploader with OCR

This is a Python application for uploading images, cropping them, and performing OCR (Optical Character Recognition) using EasyOCR library.

## Features

- Upload an image from your local file system.
- Crop the uploaded image.
- Perform OCR on the cropped region.
- Display the OCR result.

## Requirements

- Python 3.x
- Tkinter
- PIL (Python Imaging Library)
- EasyOCR

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/image-uploader-ocr.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. Click on the "Upload Image" button to select an image file from your local system.
3. After uploading, click and drag on the image to select the region for cropping.
4. Release the mouse button to finish cropping.
5. Click on the "Perform OCR" button to perform OCR on the cropped region.
6. View the OCR result displayed on the console.

## Roadmap

- [ ] Implement error handling and edge cases.
- [ ] Improve user interface with better feedback and instructions.
- [ ] Add support for additional OCR libraries.
- [ ] Enhance cropping functionality for better accuracy.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
