import os
import pytesseract

from pypdf import PdfReader
from pdf2image import convert_from_path


def extract_content_pages_to_str(file):
    content = ""

    if not os.path.exists(file) and os.path.isfile(file):
        return content

    reader = PdfReader(file)
    for num_page in range(reader.get_num_pages()):
        content += reader.pages[num_page].extract_text()
    return content


def ocr_extract_content_to_str(file):
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
    images = convert_from_path(file)

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    all_text = []
    for i, image in enumerate(images):
        temp_image_path = os.path.join(temp_dir, f"page_{i + 1}.png")
        image.save(temp_image_path, "PNG")
        text = pytesseract.image_to_string(image)
        all_text.append(text)
        os.remove(temp_image_path)

    content = "\n".join(all_text)
    return content
