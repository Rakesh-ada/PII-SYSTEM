from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_images(image_paths):
    """
    Extract text from multiple images using OCR and combine the results.
    
    :param image_paths: List of image file paths
    :return: Combined text extracted from all images
    """
    combined_text = ""
    try:
        for image_path in image_paths:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            combined_text += text + "\n"  # Add a newline between texts from each image
        return combined_text.strip()  # Remove trailing newline
    except Exception as e:
        print(f"Error extracting text from images: {e}")
        return ""

# Example usage
if __name__ == "__main__":
    image_paths = ["image1.png", "image2.png"]
    extracted_text = extract_text_from_images(image_paths)
    print("Combined Text from Images:")
    print(extracted_text)
