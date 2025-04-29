import rasterio
import numpy as np
import glob
import os

folder_path = r"C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_WaPOR"

tif_files = sorted(glob.glob(os.path.join(folder_path, "*.tif")))

with rasterio.open(tif_files[0]) as src0:
    meta = src0.meta.copy()
    annual_npp = np.zeros(src0.read(1).shape, dtype=float)

for tif_file in tif_files:
    with rasterio.open(tif_file) as src:
        data = src.read(1).astype(float)
        data[data == src.nodata] = np.nan
        annual_npp += np.nan_to_num(data)

# Multiply the values by 10 to make it annual
annual_npp = annual_npp * 10

# Apply scale factor
annual_npp = annual_npp * 0.001


output_path = os.path.join(folder_path, "Annual_NPP_BE_Lon_WaPOR.tif")

meta.update(dtype=rasterio.float32)

with rasterio.open(output_path, 'w', **meta) as dst:
    dst.write(annual_npp.astype(np.float32), 1)

print("Annual_NPP_Created with Scale Factor:", output_path)
