from PIL import Image
import os


def process_file(file_path):
    # Resize or adjust image quality for better stenography embedding
    if file_path.lower().endswith(("png", "jpg", "jpeg")):
        img = Image.open(file_path)
        img = img.resize((img.width // 2, img.height // 2))  # Example resize
        img.save(file_path)


# More functions to handle PDFs or DOCX files if needed
