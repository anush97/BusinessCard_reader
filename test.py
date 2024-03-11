import cv2
import pytesseract
import spacy

# Load the spaCy model
nlp = spacy.load("output/model-last")

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
 
    return image

def extract_text_from_image(image):
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def tag_and_print_entities(text):
    # Process the text with the trained spaCy model
    doc = nlp(text)
    # Print detected entities
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")

def evaluate_image(image_path):
    preprocessed_image = preprocess_image(image_path)
    extracted_text = extract_text_from_image(preprocessed_image)
    tag_and_print_entities(extracted_text)

# Specify the path to your image file
image_path = 'data/mom.jpeg'
evaluate_image(image_path)
