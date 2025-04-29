import rasterio
import numpy as np
import glob
import os

folder_path = "C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_MODIS17"
tif_files = sorted(glob.glob(os.path.join(folder_path, "*.tif")))


# 2. Tüm .tif dosyalarının listesini al
tif_files = sorted(glob.glob(os.path.join(folder_path, "*.tif")))

# 3. Her tif dosyasını aç, 1000 ile çarp, yeni dosya olarak kaydet
for tif_file in tif_files:
    with rasterio.open(tif_file) as src:
        data = src.read(1).astype(float)
        meta = src.meta.copy()
        
        # NoData'yı koru
        data[data == src.nodata] = np.nan
        
        # ✅ kgC → gC çevirisi: 1000 ile çarp
        data_converted = data * 0.1

    # Yeni dosya ismi oluştur
    filename = os.path.basename(tif_file)
    output_path = os.path.join(folder_path, f"converted_{filename}")
    
    # GeoTIFF olarak kaydet
    meta.update(dtype=rasterio.float32)

    with rasterio.open(output_path, 'w', **meta) as dst:
        dst.write(data_converted.astype(np.float32), 1)

    print(f"Converted: {output_path}")
