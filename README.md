# Real Estate Price Prediction using Satellite Imagery

This project integrates traditional tabular real estate data (square footage, location, etc.) with **visual signals extracted from satellite imagery** to predict house prices.

While standard Deep Learning (ResNet) struggled with high-dimensional noise, we successfully utilized **Explicit Feature Engineering** (Computer Vision via OpenCV) to extract interpretable metrics—such as Vegetation Index, Water Presence, and Edge Density—to quantify "Curb Appeal."

**Final Result:** The Ensemble Model achieved an **R² of ~0.89**, outperforming the tabular baseline.

## 📂 Project Structure

| File | Description |
| --- | --- |
| `main.ipynb` | **Main Notebook**. Contains EDA, Image Feature Extraction (OpenCV), Model Training (XGBoost), and Grad-CAM Analysis. |
| `data_fetcher.py` | Script to download satellite imagery tiles (Zoom Level 18) based on Lat/Long coordinates in the CSVs. |
| `audit_coordinates.py` | Utility script to verify downloaded images and identify corrupt/0KB files. |
| `missing_data.py` | Helper script to handle missing values or skipped downloads. |
| `coordinate_to_url_test.py` | Unit test to verify the logic converting Lat/Long to Map Tile URLs. |
| `train.csv` / `test.csv` | The raw tabular dataset containing house features and IDs. |
| `requirements.txt` | List of Python dependencies required to run the project. |

## 🚀 Setup & Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/sat_image_property_valuation.git
cd sat_image_property_valuation

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```



## 🛠️ Usage Guide

### Step 1: Download Satellite Imagery

Before training, you need to fetch the images corresponding to the house coordinates.

```bash
python data_fetcher.py

```

* *Note:* This script handles rate limiting and header rotation to download tiles from the map server.
* *Output:* Creates an `images/` directory with `train/` and `test/` subfolders.

### Step 2: Audit Data (Optional)

Ensure all images downloaded correctly and remove empty files.

```bash
python audit_coordinates.py

```

### Step 3: Train & Analyze

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