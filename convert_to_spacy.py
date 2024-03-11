'''import spacy
from spacy.tokens import DocBin
import json
from sklearn.model_selection import train_test_split

nlp = spacy.blank("en")  # Load a blank English model

def convert_to_spacy_format(data, filename):
    doc_bin = DocBin()
    for text, annotations in data:
        doc = nlp.make_doc(text)
        ents = []
        current_end = -1  # Track end position of the last entity
        for start, end, label in annotations['entities']:
            if start < current_end:
                # Print overlapping entities
                print(f"Overlap detected: Text='{text[start:end]}' Label='{label}' conflicts with entity ending at position {current_end}")
            else:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is not None:
                    ents.append(span)
                    current_end = end  # Update the last entity's end position
        doc.ents = ents
        doc_bin.add(doc)
    doc_bin.to_disk(filename)

# Load the annotated data
with open("training_data.json", "r") as f:
    TRAIN_DATA = json.load(f)

# Split the data into training and test sets
train_data, test_data = train_test_split(TRAIN_DATA, test_size=0.2)

# Convert and save the training and test data
convert_to_spacy_format(train_data, "train.spacy")
convert_to_spacy_format(test_data, "test.spacy")
'''
import spacy
from spacy.tokens import DocBin
import json
from sklearn.model_selection import train_test_split

nlp = spacy.blank("en")  # Load a blank English model

def convert_to_spacy_format(data, filename):
    doc_bin = DocBin()

    for text, annotations in data:
        doc = nlp.make_doc(text)
        ents = []

        # Sort and merge overlapping entities
        annotations['entities'] = sorted(annotations['entities'], key=lambda e: e[0])
        merged_ents = []
        for start, end, label in annotations['entities']:
            if merged_ents and start <= merged_ents[-1][1]:
                merged_ents[-1] = (merged_ents[-1][0], max(end, merged_ents[-1][1]), label)
            else:
                merged_ents.append((start, end, label))
        
        for start, end, label in merged_ents:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is not None:
                ents.append(span)

        doc.ents = ents
        doc_bin.add(doc)

    doc_bin.to_disk(filename)


# Load the annotated data
with open("training_data.json", "r") as f:
    TRAIN_DATA = json.load(f)

# Split the data into training and test sets
train_data, test_data = train_test_split(TRAIN_DATA, test_size=0.2)

# Convert and save the training and test data
convert_to_spacy_format(train_data, "train.spacy")
convert_to_spacy_format(test_data, "test.spacy")
