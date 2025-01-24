# PII Extraction and QR Code Generator

This project is a powerful tool designed to extract Personally Identifiable Information (PII) from PDF documents and images, detect sensitive data, and generate visually engaging QR code cards for securely sharing this information. 

## Key Features

- **PII Extraction**: Automatically detects PII such as Aadhaar details from both PDF files and images.
- **QR Code Generation**: Creates QR codes for securely sharing the extracted information or file URLs.
- **Vibrant PII Cards**: Generates visually appealing cards with PII details and a QR code, complete with rounded corners and stylish margins.
- **Pinata Integration**: Uploads images to IPFS via Pinata and retrieves a secure URL.
- **Custom Styling**: Supports vibrant text, customizable colors, and dynamic layouts for a professional appearance.

## How It Works

1. **Process Images**: Extract text and detect PII from images using integrated modules.
2. **Upload to Pinata**: Automatically upload files to IPFS and retrieve a secure link.
3. **Generate QR Code**: Create a QR code linking to the secure URL or extracted PII data.
4. **Create PII Card**: Combine the extracted data and QR code into a visually appealing card with customizable styles and vibrant colors.

## Technologies Used

- **Python Libraries**:
  - `qrcode`: For generating QR codes.
  - `Pillow`: For creating and styling PII cards.
  - `PyPDF2`: For extracting text from PDFs.
  - `requests`: For uploading files to Pinata.
- **IPFS & Pinata**: For secure and decentralized file storage.

## Use Cases

- **Aadhaar Management**: Securely share Aadhaar details with authorized personnel.
- **Document Verification**: Extract and verify PII from official documents.
- **Secure Data Sharing**: Use QR codes to securely share sensitive information without exposing it directly.

## Customization

- Easily change the colors, fonts, and layout of the generated PII card.
- Adjust QR code placement and size for different use cases.
- Integrate additional PII detection modules as needed.

## Getting Started

Follow the steps below to set up and run the project:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the `main.py` script to process files and generate PII cards:
   ```bash
   python main.py
   ```

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to enhance functionality or fix bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
