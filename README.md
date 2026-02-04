# geospatial-raster

A hands-on practice repository for Module 6, focused on core geospatial concepts using a small synthetic raster dataset. The project demonstrates GeoTIFF-style multi-band rasters, pixel-level spectrum extraction, spectral signatures, and simple indices.

## Project Structure

```
geospatial-raster/
  README.md
  src/
    synthetic_raster_spectral_signature.py
  data/
    synthetic_pixel_spectrum.csv
```

## M6: Geospatial Data Practice (Synthetic Raster + Spectral Signature)

This project is a simple practice setup for Module 6 concepts:
- What geospatial data represents (location, attributes, time)
- Raster vs vector thinking
- Multi-band raster structure (bands, rows, columns)
- Extracting a pixel spectrum using (row, col)
- Plotting spectral signatures
- Basic georeferencing with an affine-style transform (row/col to lon/lat)
- Optional NDVI calculation using Red and NIR bands

## What's inside

- `src/synthetic_raster_spectral_signature.py`
  - Creates a small 3×3 synthetic multi-band raster with six bands: Blue, Green, Red, NIR, SWIR1, SWIR2
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
```

## Usage

Run the main script:
```bash
python src/synthetic_raster_spectral_signature.py
```

This will:
1. Generate a synthetic 3×3 raster with 6 spectral bands
2. Extract the spectral signature at pixel (1, 2)
3. Display the pixel's geographic coordinates (lat/lon)
4. Plot the spectral signature curve
5. Calculate NDVI (Normalized Difference Vegetation Index)
6. Save results to `data/synthetic_pixel_spectrum.csv` and `spectral_signature.png`

## Band Information

| Band | Central Wavelength (nm) | Spectral Range (nm) |
|------|------------------------|---------------------|
| Blue | 490 | 450-510 |
| Green | 560 | 520-600 |
| Red | 665 | 630-690 |
| Near Infrared (NIR) | 865 | 760-900 |
| Shortwave Infrared 1 (SWIR1) | 1610 | 1550-1750 |
| Shortwave Infrared 2 (SWIR2) | 2200 | 2100-2300 |

## Learning Outcomes

After completing this practice, you should understand:
- How raster data is structured as arrays with bands, rows, and columns
- How to extract and work with spectral signatures from raster data
- The relationship between pixel indices and geographic coordinates
- How to calculate simple spectral indices like NDVI
