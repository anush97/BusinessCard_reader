import numpy as np
import pandas as pd
import cv2
import pytesseract
import os
from glob import glob
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore")

# List to hold all image paths
imgPaths = []

# Extensions to look for
extensions = ['*.png', '*.jpg', '*.jpeg']

# Directory to search in
directory = "data/"

# Gather all image paths
for extension in extensions:
    imgPaths.extend(glob(directory + extension))

# Initialize a DataFrame to hold all business card data
allBusinessCard = pd.DataFrame(columns=["id", "text"])

for imgpath in tqdm(imgPaths, desc="BusinessCard"):
    _, filename = os.path.split(imgpath)

    # Extract data and text
    image = cv2.imread(imgpath)
    data = pytesseract.image_to_data(image)

    dataList = list(map(lambda x: x.split("\t"), data.split("\n")))
    df = pd.DataFrame(dataList[1:], columns=dataList[0])
    df.dropna(inplace=True)
    df["conf"] = df["conf"].astype(float)
    df["conf"] = df["conf"].astype(int)

    usefulData = df.query("conf >= 30")

    # DataFrame which contains the useful information that is required for labeling
    businessCard = pd.DataFrame()
    businessCard["text"] = usefulData["text"]
    businessCard["id"] = filename
    
    # Concatenation
    allBusinessCard = pd.concat((allBusinessCard, businessCard))

# Save the collected data to a TSV file
allBusinessCard.to_csv("businessCard.csv", index=False, sep="\t")
