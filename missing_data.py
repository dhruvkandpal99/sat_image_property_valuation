### This code is to help you identify which images didn't donwload.
### It scans the directory for the id of each images from the csv file and if not found, puts that id in a csv
### The csv can then be used to easily download the remaining images.
### This is necessary as sometimes due to hitting server limit, you might just be downloading 0/1 kb files with the same names

import pandas as pd
import os
from pathlib import Path

# Config
TRAIN_CSV = "/Users/dhruvkandpal/Documents/pythonProjects/env/cdc/train.csv"
TRAIN_IMG_DIR = Path("images/train")

print("--- auditing download status ---")

# Load Data
df = pd.read_csv(TRAIN_CSV)
total_rows = len(df)
found_count = 0
missing_ids = []

# Check every file
for index, row in df.iterrows():
    img_path = TRAIN_IMG_DIR / f"{row['id']}.jpg"
    if img_path.exists() and img_path.stat().st_size > 1000: # Check exist AND size > 1KB
        found_count += 1
    else:
        missing_ids.append(row)

# Report
print(f"Total Rows in CSV: {total_rows}")
print(f"Images Successfully Downloaded: {found_count}")
print(f"Missing / Corrupt Images: {len(missing_ids)}")

# Save the missing list for a retry
if len(missing_ids) > 0:
    missing_df = pd.DataFrame(missing_ids)
    missing_df.to_csv("missing_train.csv", index=False)
    print("✓ Saved 'missing_train.csv'. Use this file to retry downloading.")
else:
    print("✓ All images are present!")