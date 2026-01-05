### We are not sure if all the coordinates given are correct, any undefined behaviour may affect our data_fetcher.py program.
### Hence, this code checks if all coordinates are valid.

import pandas as pd
import matplotlib.pyplot as plt

def audit_coordinates(csv_path, expected_bounds=None):
    print(f"\n--- Auditing {csv_path} ---")
    df = pd.read_csv(csv_path)
    
    # 1. Check for Missing Data (NaNs)
    missing = df[['lat', 'long']].isnull().sum().sum()
    if missing > 0:
        print(f"⚠ FOUND {missing} missing values!")
    else:
        print("✓ No missing values.")

    # 2. Check Mathematical Bounds
    # Lat must be -90 to 90. Long must be -180 to 180.
    bad_lat = df[~df['lat'].between(-90, 90)]
    bad_lon = df[~df['long'].between(-180, 180)]
    
    if len(bad_lat) > 0 or len(bad_lon) > 0:
        print(f"⚠ FOUND MATHEMATICALLY IMPOSSIBLE COORDINATES:")
        print(f"  - Invalid Lats: {len(bad_lat)}")
        print(f"  - Invalid Longs: {len(bad_lon)}")
    else:
        print("✓ All coordinates are mathematically valid.")

    # 3. Check Geographical Logic (Bounding Box)
    # If your data is King County (Seattle), it should be roughly:
    # Lat: 47.1 to 47.8, Long: -122.5 to -121.0
    if expected_bounds:
        min_lat, max_lat, min_lon, max_lon = expected_bounds
        outliers = df[
            (df['lat'] < min_lat) | (df['lat'] > max_lat) |
            (df['long'] < min_lon) | (df['long'] > max_lon)
        ]
        
        if len(outliers) > 0:
            print(f"⚠ FOUND {len(outliers)} LOCATION OUTLIERS (Outside expected area).")
            # Print the first few to inspect
            print(outliers[['id', 'lat', 'long']].head())
            
            # VISUALIZATION: Plot valid vs outliers
            plt.figure(figsize=(10, 6))
            plt.scatter(df['long'], df['lat'], alpha=0.5, s=2, label='Valid Data')
            plt.scatter(outliers['long'], outliers['lat'], color='red', s=10, label='Outliers')
            plt.title(f"Coordinate Distribution for {csv_path}")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.legend()
            plt.show()
        else:
            print("✓ All coordinates fall within the expected bounding box.")

# --- RUN THE AUDIT ---

# King County (Seattle Area) approximate bounding box
# Format: (min_lat, max_lat, min_lon, max_lon)
SEATTLE_BOUNDS = (47.1, 47.8, -122.6, -121.0)

audit_coordinates("/Users/dhruvkandpal/Documents/pythonProjects/env/cdc/test.csv", expected_bounds=SEATTLE_BOUNDS)