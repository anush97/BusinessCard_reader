import pandas as pd
import spacy
import re
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define the custom rule-based tagging function
def custom_rule_tagging(text):
    # Initialize an empty list for entities
    entities = []

    # Email pattern
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    for match in email_pattern.finditer(text):
        entities.append((match.start(), match.end(), 'EMAIL'))

    # Website pattern
    website_pattern = re.compile(r'\b(http://www\.|https://www\.|http://|https://|www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(/.*)?\b')
    for match in website_pattern.finditer(text):
        entities.append((match.start(), match.end(), 'WEB'))

    # Phone pattern
    phone_pattern = re.compile(r'(?:T:|Mob:|\+)?\d[\d \-()]{7,}\d')
    for match in phone_pattern.finditer(text):
        entities.append((match.start(), match.end(), 'PHONE'))

        
    # Designation pattern 
    designation_pattern = re.compile(r'\b(CEO|CTO|CFO|Manager|Director|Executive|Vice President|V\.?P\.?|President|Chairman|Supervisor|Lead|Coordinator|Analyst|Specialist|Consultant)\b', re.IGNORECASE)
    for match in designation_pattern.finditer(text):
        entities.append((match.start(), match.end(), 'DES'))
    
    # Organization pattern
    '''org_pattern = re.compile(r'\b[A-Z][a-z]*\b(?:\s[A-Z][a-z]*)*\b')
    for match in org_pattern.finditer(text):
        entities.append((match.start(), match.end(), 'ORG'))'''

    # Address pattern
    #address_pattern = re.compile(r'\b\d{1,3}\s\w+\s\w+\b.*?(?:\b(?:Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chhattisgarh|Goa|Gujarat|Haryana|Himachal Pradesh|Jharkhand|Karnataka|Kerala|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal)\b),\s?(?:\b(?:India|USA|United States|Canada|Australia|UK|United Kingdom|Germany|France|Japan|China|Russia|Brazil|South Africa|Italy|Spain|Mexico|South Korea)\b)?')
    address_pattern = re.compile(r'\b\d{1,3}\s\w+\s\w+\b.*?(?:\b(?:Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chhattisgarh|Goa|Gujarat|Haryana|Himachal Pradesh|Jharkhand|Karnataka|Kerala|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|New South Wales|Queensland|Victoria|Dubai|British Columbia|Alberta|Ontario|California|Texas|New York|Florida|Illinois|Tokyo|Osaka|Kyoto|Beijing|Shanghai|Guangdong|Moscow|St. Petersburg|Sao Paulo|Rio de Janeiro|Alberta|Quebec|Ontario|New South Wales|Victoria|Sao Paulo|Gauteng|Western Cape)\b),\s?(?:\b(?:India|USA|U.A.E.|United States|Canada|Australia|UK|United Kingdom|Germany|France|Japan|China|Russia|Brazil|South Africa|Italy|Spain|Mexico|South Korea|Brazil|Australia|Canada|Japan|China|Russia|South Africa|UK|USA)\b)?')

    for match in address_pattern.finditer(text):
        entities.append((match.start(), match.end(), 'ADD'))

    return entities

# Load the CSV file
df = pd.read_csv("businessCard.csv", sep="\t")

# Aggregate text by 'id'
grouped_data = df.groupby('id')['text'].apply(lambda texts: ' '.join(texts.strip() for texts in texts)).reset_index()

# List to store the training data
training_data = []

# Process each entry in the grouped data
for _, row in grouped_data.iterrows():
    # Get custom entities using rule-based tagging
    custom_entities = custom_rule_tagging(row['text'])

    # Create a spacy document
    doc = nlp(row['text'])

    # List to store entities
    entities = []

    # Update entities with custom rule-based entities
    entities.extend(custom_entities)

    # Update entities with spaCy's named entities
    for ent in doc.ents:
        if ent.label_ in ["PERSON"]:
            entities.append((ent.start_char, ent.end_char, "NAME"))
        elif ent.label_ in ["ORG"]:
            entities.append((ent.start_char, ent.end_char, "ORG"))
        elif ent.label_ in ["GPE", "LOC","CARDINAL"]:
            entities.append((ent.start_char, ent.end_char, "ADD"))

    # Sort entities to ensure they are in the correct order
    entities = sorted(entities, key=lambda entry: entry[0])

    # Append to the training data list
    training_data.append((row['text'], {"entities": entities}))

# Save the training data to a file
with open("training_data.json", "w") as f:
    json.dump(training_data, f, ensure_ascii=False, indent=2)

print("Training data has been saved to training_data.json")
