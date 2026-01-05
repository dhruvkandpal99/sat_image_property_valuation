# Real Estate Price Prediction using Satellite Imagery

This project integrates traditional tabular real estate data (square footage, location, etc.) with **visual signals extracted from satellite imagery** to predict house prices.

While standard Deep Learning (ResNet) struggled with high-dimensional noise, we successfully utilized **Explicit Feature Engineering** (Computer Vision via OpenCV) to extract interpretable metrics — such as Vegetation Index, Water Presence, and Edge Density — to quantify "Curb Appeal."

**Final Result:** The Ensemble Model achieved an **R² of ~0.89**, outperforming the tabular baseline.

## 📂 Project Structure

| File | Description |
| --- | --- |
| `main.ipynb` | **Main Notebook**. Contains EDA, Image Feature Extraction (OpenCV), Model Training (XGBoost), and Grad-CAM Analysis. |
| `audit_coordinates.py` | **Validation Script**. Runs first to verify that all Lat/Long coordinates in the CSVs are valid before attempting downloads. |
| `coordinate_to_url_test.py` | **Diagnostic Tool**. Checks if your IP address is blocked by the map server and verifies the tile generation logic (Lat/Long  URL) is correct. |
| `data_fetcher.py` | **Downloader**. Fetches satellite imagery tiles (Zoom Level 18) for valid coordinates. |
| `missing_data.py` | **Cleanup & Tracking**. Identifies images that failed to download and detects/removes corrupt (0KB/1KB) "ghost" files. |
| `train.csv` / `test.csv` | The raw tabular dataset containing house features and IDs. |
| `requirements.txt` | List of Python dependencies required to run the project. |

## 🚀 Setup & Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```



## 🛠️ Usage Guide

### Step 1: Pre-Download Checks

First, ensure your coordinate data is valid:

```bash
python audit_coordinates.py

```

Then, run a connection test to ensure your IP isn't banned and the tile logic works:

```bash
python coordinate_to_url_test.py

```

### Step 2: Download Satellite Imagery

Fetch the images. This script handles rate limiting and header rotation.

```bash
python data_fetcher.py

```

### Step 3: Verify Integrity

After downloading, check for missing files or corrupt (0KB) downloads that need to be retried:

```bash
python missing_data.py

```

### Step 4: Train & Analyze

Open the main notebook to run the full pipeline:

```bash
jupyter notebook main.ipynb

```

**Key Steps in the Notebook:**

1. **Visual Feature Extraction:** Uses OpenCV to calculate `Greenery_Score` (Vegetation), `Water_Score`, and `Edge_Density` (Neighborhood complexity).
2. **Modeling:** Trains an XGBoost regressor on the combined dataset (Tabular + Visual Features).
3. **Explainability:** Generates Grad-CAM heatmaps to visualize model attention on specific properties.
4. **Submission:** Generates `submission_ensemble.csv`.

## 🧠 Methodology

* **Hypothesis:** Satellite imagery contains latent "value" signals (privacy, nature, density) missed by spreadsheets.
* **Approach:**
* *Deep Learning:* Initial ResNet18 approach suffered from the "Curse of Dimensionality" (R² 0.86).
* *Smart Metrics:* Pivoted to calculating explicit visual features. High greenery and low edge density (indicative of large private lots) correlated with higher prices.


* **Model:** XGBRegressor with Early Stopping.
* **Validation:** Achieved lower RMSE ($117k vs $119k) compared to the tabular-only baseline.

## 📊 Requirements

* Python 3.8+
* `xgboost`
* `opencv-python`
* `torch` / `torchvision`
* `pandas` / `numpy`
* `mercantile` (for tile calculations)

See `requirements.txt` for exact versions.
