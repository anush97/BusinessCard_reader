# BusinessCard_reader - Business Card Information Extractor

This project provides a Flask-based web application that allows users to upload business card images, extracts relevant information using Optical Character Recognition (OCR) and a pre-trained spaCy model, and offers an interface for user verification before saving the data to an Excel file.

## Features

- Image upload for business cards.
- OCR to convert images to text.
- Entity extraction using spaCy for predefined labels (e.g., NAME, DES, ORG, etc.).
- User interface for verifying and editing extracted data.
- Saving verified data to an Excel file, with the option to download.

## Installation

Ensure you have Python installed, then clone this repository and install the required dependencies:

```bash
git clone <your-repo-link>
cd <your-project-directory>
pip install -r requirements.txt
```

## Usage

To run the application:

```bash
python app.py
```

Navigate to `http://127.0.0.1:5000/` in your web browser to access the application.

## Project Structure

- `app.py`: The main Flask application file.
- `templates/`: Contains HTML templates for the web interface.
  - `index.html`: The homepage with the image upload form.
  - `verify.html`: Displays extracted information for user verification.
- `uploads/`: Directory for temporarily storing uploaded images (created on the first run).
- `verified_data.xlsx`: Excel file where verified information is stored (created after first verification).


## License

[MIT License](LICENSE)

