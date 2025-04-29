import rasterio
import numpy as np
import glob
import os

folder_path = "C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_MODIS17"
tif_files = sorted(glob.glob(os.path.join(folder_path, "*.tif")))


tif_files = sorted(glob.glob(os.path.join(folder_path, "*.tif")))

for tif_file in tif_files:
    with rasterio.open(tif_file) as src:
        data = src.read(1).astype(float)
        meta = src.meta.copy()
        
        data[data == src.nodata] = np.nan
        
        # Convert kgC to gC and apply scale factor
        data_converted = data * 0.1

    filename = os.path.basename(tif_file)
    output_path = os.path.join(folder_path, f"converted_{filename}")
    
    meta.update(dtype=rasterio.float32)

    with rasterio.open(output_path, 'w', **meta) as dst:
        dst.write(data_converted.astype(np.float32), 1)

    print(f"Converted: {output_path}")
