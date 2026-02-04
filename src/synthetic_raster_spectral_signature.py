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

df = pd.DataFrame(
    {"Band": BANDS, "Wavelength_nm": WAVELENGTH_NM, "Reflectance": pixel_spectrum}
).sort_values("Wavelength_nm")

print(f"\nCRS: {CRS}")
print(f"Pixel (row={row}, col={col}) center coordinate: lon={lon:.5f}, lat={lat:.5f}\n")
print(df.to_string(index=False))

# Save to CSV
csv_path = "data/synthetic_pixel_spectrum.csv"
df.to_csv(csv_path, index=False)
print(f"\nSpectral data saved to: {csv_path}")

# ----------------------------
# 5) Plot spectral signature
# ----------------------------
plt.figure(figsize=(10, 6))
plt.plot(df["Wavelength_nm"], df["Reflectance"], marker="o", linewidth=2, markersize=8)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance")
plt.title(f"Spectral Signature at pixel (row={row}, col={col})")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("spectral_signature.png", dpi=100)
print("Spectral signature plot saved to: spectral_signature.png")
plt.show()

# ----------------------------
# 6) NDVI calculation
# ----------------------------
nir = df.loc[df["Band"] == "NIR", "Reflectance"].iloc[0]
red = df.loc[df["Band"] == "Red", "Reflectance"].iloc[0]
ndvi = (nir - red) / (nir + red)

print(f"\nNDVI at (row={row}, col={col}): {ndvi:.4f}")

# ----------------------------
# 7) Show raster band statistics
# ----------------------------
print("\n--- Raster Band Statistics ---")
for b, band_name in enumerate(BANDS):
    band_data = raster[b]
    print(
        f"{band_name:8s}: min={band_data.min():.4f}, max={band_data.max():.4f}, mean={band_data.mean():.4f}"
    )
