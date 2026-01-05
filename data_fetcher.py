### This converts the coordinates to tiles, downloads the image from the server and then puts the image in the folder.
### This script is slow to run (3-4 hrs) to ensure that you don't hit server limit.

import pandas as pd
import requests
import os
import mercantile
import time
import shutil
from pathlib import Path

# --- CONFIGURATION ---
ZOOM_LEVEL = 18 
TILE_SERVER = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
BASE_DIR = Path("images")
TRAIN_DIR = BASE_DIR / "train"
TEST_DIR = BASE_DIR / "test"

# Header rotation (Helps avoid detection)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
}

def setup_directories():
    os.makedirs(TRAIN_DIR, exist_ok=True)
    os.makedirs(TEST_DIR, exist_ok=True)

def fetch_tile(lat, lon, house_id, save_folder):
    file_path = save_folder / f"{house_id}.jpg"
    
    # --- SMART SKIP LOGIC ---
    # Only skip if file exists AND is a valid size (> 3KB)
    if file_path.exists():
        if file_path.stat().st_size > 3000: 
            return "Skipped"
        else:
            # If it's tiny, delete it and retry
            os.remove(file_path)

    try:
        tile = mercantile.tile(lon, lat, ZOOM_LEVEL)
        url = TILE_SERVER.format(z=ZOOM_LEVEL, y=tile.y, x=tile.x)
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            return "Success"
        else:
            return f"Error {response.status_code}"
            
    except Exception as e:
        return f"Failed: {e}"

def process_dataset(csv_name, output_folder, label):
    if not os.path.exists(csv_name):
        return

    print(f"\n--- Processing {label} Data ---")
    df = pd.read_csv(csv_name)
    total = len(df)
    
    count = 0
    downloaded = 0
    
    for index, row in df.iterrows():
        status = fetch_tile(row['lat'], row['long'], row['id'], output_folder)
        
        count += 1
        if status == "Success":
            downloaded += 1
            # Only sleep if we actually downloaded something
            time.sleep(0.5) 
            
        if count % 100 == 0:
            print(f"[{label}] Checked {count}/{total} - New Downloads: {downloaded}")

if __name__ == "__main__":
    setup_directories()
    process_dataset("/Users/dhruvkandpal/Documents/pythonProjects/env/cdc/missing_train.csv", TRAIN_DIR, "Train")
    # process_dataset("/Users/dhruvkandpal/Documents/pythonProjects/env/cdc/test.csv", TEST_DIR, "Test")
    print("\nDone. Run 'find images -size -3k' to verify no corrupt files remain.")