# geospatial-raster
A hands-on practice repo for Module 6 covering geospatial data concepts, GeoTIFF-style multi-band rasters, pixel spectrum extraction, spectral signatures, and basic indices using a small synthetic dataset.

m6-geospatial-raster-practice/
  README.md
  src/
    synthetic_raster_spectral_signature.py
  data/
    synthetic_pixel_spectrum.csv


# M6: Geospatial Data Practice (Synthetic Raster + Spectral Signature)

This mini project is a practice sandbox for Module 6 concepts:
- What geospatial data is (location + attributes + time)
- Raster vs vector mental models
- GeoTIFF-style multi-band rasters (bands, rows, cols)
- Extracting a pixel spectrum by (row, col)
- Plotting a spectral signature
- Simple georeferencing using an affine transform (row/col -> lon/lat)
- Optional: NDVI calculation from Red and NIR bands

## What’s inside

- `src/synthetic_raster_spectral_signature.py`
  - Creates a tiny 3x3 fake multi-band raster array with 6 bands:
    Blue, Green, Red, NIR, SWIR1, SWIR2
  - Extracts the spectrum for one pixel (row, col)
  - Converts (row, col) to approximate lon/lat using a GeoTIFF-style transform
  - Plots the spectral signature
  - Computes NDVI

- `data/synthetic_pixel_spectrum.csv`
  - A simple band table for one pixel (like a single pixel’s band values)

## Requirements

Python 3.9+ recommended.

Install dependencies:
```bash
pip install numpy pandas matplotlib


python src/synthetic_raster_spectral_signature.py


---

## src/synthetic_raster_spectral_signature.py
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 1) Band metadata (like a multispectral GeoTIFF)
# ----------------------------
BANDS = ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]
WAVELENGTH_NM = np.array([490, 560, 665, 865, 1610, 2200])

N_BANDS = len(BANDS)
ROWS, COLS = 3, 3

# ----------------------------
# 2) Create a fake raster stack: shape = (bands, rows, cols)
# ----------------------------
# Base reflectance values (one "typical" pixel spectrum)
BASE = np.array([0.12, 0.18, 0.22, 0.46, 0.31, 0.27])

rng = np.random.default_rng(42)
raster = np.zeros((N_BANDS, ROWS, COLS), dtype=float)

for b in range(N_BANDS):
    # small gradient across 3x3 + tiny noise
    grad = (np.arange(ROWS).reshape(-1, 1) * 0.01) + (np.arange(COLS) * 0.005)
    noise = rng.normal(0, 0.002, size=(ROWS, COLS))
    raster[b] = BASE[b] + grad + noise

raster = np.clip(raster, 0, 1)

print("Raster shape (bands, rows, cols):", raster.shape)

# ----------------------------
# 3) GeoTIFF-style georeferencing (Affine transform + CRS)
# ----------------------------
CRS = "EPSG:4326"          # pretend lon/lat
X0, Y0 = -59.0, 15.0       # top-left corner (lon, lat)
XRES, YRES = 0.01, 0.01    # pixel size in degrees


def rowcol_to_xy(row: int, col: int, x0: float, y0: float, xres: float, yres: float, center: bool = True):
    """
    Convert (row, col) to map coordinates using a simple affine transform.
    If center=True, return the pixel center coordinate.
    """
    if center:
        x = x0 + (col + 0.5) * xres
        y = y0 - (row + 0.5) * yres
    else:
        x = x0 + col * xres
        y = y0 - row * yres
    return x, y


# ----------------------------
# 4) Extract a pixel spectrum by (row, col)
# ----------------------------
row, col = 1, 2  # choose any pixel within 0..2
pixel_spectrum = raster[:, row, col]  # key extraction (bands, row, col)

lon, lat = rowcol_to_xy(row, col, X0, Y0, XRES, YRES, center=True)

df = pd.DataFrame({
    "Band": BANDS,
    "Wavelength_nm": WAVELENGTH_NM,
    "Reflectance": pixel_spectrum
}).sort_values("Wavelength_nm")

print(f"\nCRS: {CRS}")
print(f"Pixel (row={row}, col={col}) approx center coordinate: lon={lon:.5f}, lat={lat:.5f}\n")
print(df.to_string(index=False))

# ----------------------------
# 5) Plot the spectral signature
# ----------------------------
plt.figure()
plt.plot(df["Wavelength_nm"], df["Reflectance"], marker="o")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance")
plt.title(f"Spectral Signature at pixel (row={row}, col={col})")
plt.grid(True)
plt.show()

# ----------------------------
# 6) Example index (NDVI)
# ----------------------------
nir = df.loc[df["Band"] == "NIR", "Reflectance"].iloc[0]
red = df.loc[df["Band"] == "Red", "Reflectance"].iloc[0]
ndvi = (nir - red) / (nir + red)

print(f"\nNDVI at (row={row}, col={col}): {ndvi:.4f}")


Band,Central_Wavelength_nm,Spectral_Range_nm,Reflectance
Blue,490,450-510,0.12
Green,560,520-600,0.18
Red,665,630-690,0.22
Near_Infrared (NIR),865,760-900,0.46
Shortwave_Infrared 1 (SWIR1),1610,1550-1750,0.31
Shortwave_Infrared 2 (SWIR2),2200,2100-2300,0.27
