import rasterio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from matplotlib.colors import LinearSegmentedColormap

# ========== 1. SET YOUR PATHS HERE ==========
WAPOR_PATH = "C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_WaPOR/Annual_NPP_BE_Lon_WaPOR.tif"
MODIS_PATH = "C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_MODIS17/aligned_MOD17_BE_Lon_Modis.tif"
# ============================================

# --- Color Schemes ---
common_cmap = LinearSegmentedColormap.from_list('common', 
                    ['#f7fcb9', '#addd8e', '#41ab5d', '#006837'], N=256)

# --- Load Rasters ---
def load_raster(path):
    with rasterio.open(path) as src:
        data = src.read(1).astype(float)
        data[data == src.nodata] = np.nan
        data[data < 0] = np.nan
    return data

print("Loading data...")
wapor = load_raster(WAPOR_PATH)
modis = load_raster(MODIS_PATH)

# --- Mask valid data ---
mask = (~np.isnan(wapor)) & (~np.isnan(modis))
wapor_vals = wapor[mask]
modis_vals = modis[mask]

# --- Calculate Differences ---
diff = modis - wapor

# --- Set Manual Ranges ---
wapor_min, wapor_max = 150, 1000
modis_min, modis_max = 300, 900
diff_abs_max = np.percentile(np.abs(diff[mask]), 95)

# --- Visualizations ---
fig, axs = plt.subplots(1, 3, figsize=(24, 6))

# Plot 1: WaPOR
im1 = axs[0].imshow(wapor, cmap=common_cmap, vmin=wapor_min, vmax=wapor_max)
plt.colorbar(im1, ax=axs[0], fraction=0.046, pad=0.04)
axs[0].set_title("WaPOR v3")
axs[0].axis('off')

# Plot 2: MODIS
im2 = axs[1].imshow(modis, cmap=common_cmap, vmin=modis_min, vmax=modis_max)
plt.colorbar(im2, ax=axs[1], fraction=0.046, pad=0.04)
axs[1].set_title("MODIS17")
axs[1].axis('off')

# Plot 3: Absolute Difference
axs[2].set_title("Spatial Differences\nGreen: MODIS17 > WaPOR v3   Red: MODIS17 < WaPOR v3", fontsize=11)
im3 = axs[2].imshow(diff, cmap='RdYlGn', vmin=-diff_abs_max, vmax=diff_abs_max)
cbar3 = plt.colorbar(im3, ax=axs[2], fraction=0.046, pad=0.04)
cbar3.set_label("Absolute Difference")
axs[2].axis('off')

plt.tight_layout()
plt.show()

# --- Scatterplot ---
plt.figure(figsize=(6,6))
plt.scatter(wapor_vals, modis_vals, alpha=0.5, s=10)
lims = [min(np.min(wapor_vals), np.min(modis_vals)), max(np.max(wapor_vals), np.max(modis_vals))]
plt.plot(lims, lims, 'k--', label='1:1 Line')
plt.xlabel("WaPOR v3")
plt.ylabel("MODIS17")
plt.title("WaPOR v3 vs MODIS17")
plt.legend()
plt.grid(True)
plt.show()

# --- Statistics ---
wapor_mean = np.mean(wapor_vals)
rmse = np.sqrt(mean_squared_error(wapor_vals, modis_vals))
rmse_pct = (rmse / wapor_mean) * 100
pearson_r = pearsonr(wapor_vals, modis_vals)[0]
pearson_r2 = pearson_r ** 2

metrics = {
    'WaPOR Mean': wapor_mean,
    'MODIS Mean': np.mean(modis_vals),
    'Bias': np.mean(modis_vals - wapor_vals),
    'Bias (%)': (np.mean(modis_vals - wapor_vals) / wapor_mean) * 100,
    'RMSE': rmse,
    'RMSE (%)': rmse_pct,
    'Pearson R': pearson_r,
    'Pearson R²': pearson_r2,
    'Valid Pixels': len(wapor_vals)
}

# --- Print Results ---
print("\nVALIDATION RESULTS")
print("="*40)
for name, val in metrics.items():
    if isinstance(val, float):
        print(f"{name}: {val:.4f}" + ("%" if "%" in name else ""))
    else:
        print(f"{name}: {val}")

# --- Diagnostics ---
if pearson_r2 < 0.3:
    print("\nWARNING: Low Pearson R² detected! Check variable alignment, units, or spatial match.")