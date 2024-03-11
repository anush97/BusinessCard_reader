from flask import Flask, request, render_template, redirect, url_for
import os
import pytesseract
from PIL import Image
import spacy
import pandas as pd
from werkzeug.utils import secure_filename
from openpyxl import load_workbook
from openpyxl import Workbook
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
EXCEL_FILE = 'extracted_data.xlsx'

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load spaCy model
nlp = spacy.load("old-output/model-last") 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part', 400
    image = request.files['image']
    if image.filename == '':
        return 'No selected image', 400
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Redirect to the extraction route, passing the filename as a query parameter
        return redirect(url_for('extract_info', filename=filename))
    else:
        return 'Invalid file type', 400

@app.route('/extract_info')
def extract_info():
    filename = request.args.get('filename')
    if not filename:
        return 'Missing data', 400
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    extracted_text = pytesseract.image_to_string(Image.open(image_path))

    doc = nlp(extracted_text)

    # Organize entities into specific categories
    info = {'NAME': '', 'DES': '', 'ORG': '', 'PHONE': '', 'ADD': '', 'EMAIL': '', 'WEB': ''}
    for ent in doc.ents:
        # Assume ent.label_ returns one of the predefined categories (NAME, DES, ORG, PHONE, ADD, EMAIL, WEB)
        # Append if multiple values exist, else assign
        if info[ent.label_]:
            info[ent.label_] += f", {ent.text}"  # Append with comma separation for multiple values
        else:
            info[ent.label_] = ent.text

    return render_template('verify.html', info=info)


@app.route('/write_excel', methods=['POST'])
def write_to_excel():
    # Headers as they appear in your Excel template
    headers = [
        'Company Name', 'Person Name', 'Designation', 
        'Address', 'Email', 'Mobile no.', 'Website', 
        'Industry (Biscuits, Dairy, Beverages Etc)'
    ]
    
    # Map form data to the correct headers
    form_to_header_mapping = {
        'ORG': 'Company Name', 
        'NAME': 'Person Name', 
        'DES': 'Designation', 
        'ADD': 'Address', 
        'EMAIL': 'Email', 
        'PHONE': 'Mobile no.', 
        'WEB': 'Website'
    }
    
    # Prepare info dictionary with blank for the 'Industry they deal in' field
    info = {header: '' for header in headers}
    for form_field, header in form_to_header_mapping.items():
        info[header] = request.form.get(form_field, '')

    # Create a DataFrame with just the new info
    df_new = pd.DataFrame([info.values()])  # We only need the values here for the new row

    try:
        # Attempt to load an existing workbook
        workbook = load_workbook(EXCEL_FILE)
        sheet = workbook.active
        
        
    except FileNotFoundError:
        # If the Excel file doesn't exist, create a new workbook and add the headers
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(headers)  # Write the headers to the first row

    # Get the last row in the existing Excel file and append the new data from the next row
    sheet.append(list(info.values()))

    try:

        workbook.save(EXCEL_FILE)
        df = pd.read_excel(EXCEL_FILE)
        excel_data_html = df.to_html(index=False, classes='excel-table')

        # Render the success.html template, passing the table's HTML
        return render_template('success.html', excel_table=excel_data_html)
    except Exception as e:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
