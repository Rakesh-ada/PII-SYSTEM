import qrcode
from PIL import Image, ImageDraw, ImageFont
from pdf_extractor import extract_text_from_pdf
from image_extractor import extract_text_from_images
from pii_detector import detect_pii
import pinata_upload

def generate_qr_code(data):
    """Generate a QR code for the given data (file path or URL)."""
    qr = qrcode.make(data)
    qr_image = qr.convert('RGB')  # Ensure it's in RGB format for Pillow compatibility
    return qr_image

def create_pii_card(pii_data, qr_image):
    """Create a card-like image with PII details and QR code."""
    # Create a blank image with vibrant background color and added margin
    card_width = 430
    card_height = 270
    margin = 7
    card = Image.new('RGB', (card_width + 2 * margin, card_height + 2 * margin), (0, 0, 0, 0))  # transparent background
    draw = ImageDraw.Draw(card)

    # Use a font (ensure the font file is available or use a default one)
    try:
        font = ImageFont.truetype("arialbd.ttf", 18)  # Make sure 'arial.ttf' exists
        font1 = ImageFont.truetype("arialbd.ttf", 22)
    except IOError:
        font = ImageFont.load_default() # Fallback to default font
        font1 = ImageFont.load_default()

    # Draw a rounded rectangle with a margin (padding inside the card)
    corner_radius = 15  # Control the roundness of the corners
    draw.rounded_rectangle(
        [(margin, margin), (card_width + margin, card_height + margin)],
        radius=corner_radius,
        fill='#EFB036',  # Match the card background color
        outline='#23486A',  # Optional outline color
        width=2
    )

    # Add title with a vibrant color
    draw.text((margin + 15, margin + 10), "AADHAAR DETAILS", font=font1, fill="#3B6790")  # Neon yellow color

    # Add the extracted PII data with more vibrant colors
    y_offset = margin + 70
    for item in pii_data:
        text = f"{item['entity']}: {item['text']}"
        draw.text((margin + 15, y_offset), text, font=font, fill="#3B6790")  # Vibrant green color
        y_offset += 30  # Space between each piece of PII data

    # Resize and position the QR code (vertically centered)
    qr_size = 130
    qr_resized = qr_image.resize((qr_size, qr_size))
    qr_x = card_width + margin - qr_size - 10
    qr_y = (card_height + margin - qr_size) // 2  # Center vertically

    # Add a border with a vibrant color around the QR code
    border_color = "#23486A"  # Vibrant blue color for the border
    border_thickness = 4
    draw.rectangle(
        [(qr_x - border_thickness, qr_y - border_thickness), 
         (qr_x + qr_size + border_thickness, qr_y + qr_size + border_thickness)],
        outline=border_color, width=border_thickness
    )

    card.paste(qr_resized, (qr_x, qr_y))

    # Save the final image to a file
    card.save('pii_card.png')

def main():
    pdf_path = "data/example.pdf"
    image_paths = ["data/images/image1.png"]
    # Process PDF
    print("\nProcessing PDF...")
    pdf_text = extract_text_from_pdf(pdf_path)
    print(pdf_text)
    
    pdf_pii = detect_pii(pdf_text)
    print("PII detected in PDF:", pdf_pii)

    # Process Images
    print("\nProcessing Images...")
    image_text = extract_text_from_images(image_paths)
    print(image_text)
    image_pii = detect_pii(image_text)
    print("PII detected in Images:", image_pii)

    # Combine PII from PDF and Images
    combined_pii = pdf_pii + image_pii

    # Generate QR code for the original file (using PDF path)
    # Call the function to upload and get the image link 
    file_to_upload = "data/images/image1.png"  #
    pinata_upload.upload_to_pinata(file_to_upload)

    # Retrieve the img value after the upload process
    img_value = pinata_upload.get_img()
    print(f"Img Value from pinata_upload: {img_value}")
    qr_image = generate_qr_code(img_value)

    # Create the PII card with the detected details and QR code
    create_pii_card(combined_pii, qr_image)

    print("PII card created and saved as 'pii_card.png'.")

if __name__ == "__main__":
    main()
