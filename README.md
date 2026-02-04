# geospatial-raster

A hands-on practice repository for Module 6, focused on core geospatial concepts using a small synthetic raster dataset. The project demonstrates GeoTIFF-style multi-band rasters, pixel-level spectrum extraction, spectral signatures, and simple indices.

m6-geospatial-raster-practice/
  README.md
  src/
    synthetic_raster_spectral_signature.py
  data/
    synthetic_pixel_spectrum.csv


# M6: Geospatial Data Practice (Synthetic Raster + Spectral Signature)

This project is a simple practice setup for Module 6 concepts:
- What geospatial data represents (location, attributes, time)
- Raster vs vector thinking
- Multi-band raster structure (bands, rows, columns)
- Extracting a pixel spectrum using (row, col)
- Plotting spectral signatures
- Basic georeferencing with an affine-style transform (row/col to lon/lat)
- Optional NDVI calculation using Red and NIR bands

## What’s inside

- `src/synthetic_raster_spectral_signature.py`
  - Creates a small 3×3 synthetic multi-band raster with six bands:
    Blue, Green, Red, NIR, SWIR1, SWIR2
  - Extracts the spectral values for a selected pixel
  - Converts pixel indices to approximate longitude and latitude
  - Plots the spectral signature
  - Computes NDVI

- `data/synthetic_pixel_spectrum.csv`
  - A simple band-level table representing reflectance values for a single pixel

## Requirements

Python 3.9 or newer is recommended.

Install dependencies:
```bash
pip install numpy pandas matplotlib

python src/synthetic_raster_spectral_signature.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 1) Band metadata (similar to a multispectral GeoTIFF)
# ----------------------------
BANDS = ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]
WAVELENGTH_NM = np.array([490, 560, 665, 865, 1610, 2200])

N_BANDS = len(BANDS)
ROWS, COLS = 3, 3

# ----------------------------
# 2) Create a synthetic raster stack: shape = (bands, rows, cols)
# ----------------------------
BASE = np.array([0.12, 0.18, 0.22, 0.46, 0.31, 0.27])

rng = np.random.default_rng(42)
raster = np.zeros((N_BANDS, ROWS, COLS), dtype=float)

for b in range(N_BANDS):
    grad = (np.arange(ROWS).reshape(-1, 1) * 0.01) + (np.arange(COLS) * 0.005)
    noise = rng.normal(0, 0.002, size=(ROWS, COLS))
    raster[b] = BASE[b] + grad + noise

raster = np.clip(raster, 0, 1)

print("Raster shape (bands, rows, cols):", raster.shape)

# ----------------------------
# 3) Simple GeoTIFF-style georeferencing
# ----------------------------
CRS = "EPSG:4326"
X0, Y0 = -59.0, 15.0
XRES, YRES = 0.01, 0.01

def rowcol_to_xy(row, col, x0, y0, xres, yres, center=True):
    if center:
        x = x0 + (col + 0.5) * xres
        y = y0 - (row + 0.5) * yres
    else:
        x = x0 + col * xres
        y = y0 - row * yres
    return x, y

# ----------------------------
# 4) Extract pixel spectrum
# ----------------------------
row, col = 1, 2
pixel_spectrum = raster[:, row, col]

lon, lat = rowcol_to_xy(row, col, X0, Y0, XRES, YRES, center=True)

df = pd.DataFrame({
    "Band": BANDS,
    "Wavelength_nm": WAVELENGTH_NM,
    "Reflectance": pixel_spectrum
}).sort_values("Wavelength_nm")

print(f"\nCRS: {CRS}")
print(f"Pixel (row={row}, col={col}) center coordinate: lon={lon:.5f}, lat={lat:.5f}\n")
print(df.to_string(index=False))

# ----------------------------
# 5) Plot spectral signature
# ----------------------------
plt.figure()
plt.plot(df["Wavelength_nm"], df["Reflectance"], marker="o")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance")
plt.title(f"Spectral Signature at pixel (row={row}, col={col})")
plt.grid(True)
plt.show()

# ----------------------------
# 6) NDVI calculation
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
