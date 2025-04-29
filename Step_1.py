import rasterio
import numpy as np
import glob
import os

# 1. Klasör yolu
folder_path = r"C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_WaPOR"

# 2. Tüm .tif dosyalarının listesini al
tif_files = sorted(glob.glob(os.path.join(folder_path, "*.tif")))

# 3. İlk rasteri aç ve boş bir array oluştur
with rasterio.open(tif_files[0]) as src0:
    meta = src0.meta.copy()
    annual_npp = np.zeros(src0.read(1).shape, dtype=float)

# 4. Bütün dosyaları oku ve üst üste topla
for tif_file in tif_files:
    with rasterio.open(tif_file) as src:
        data = src.read(1).astype(float)
        data[data == src.nodata] = np.nan
        annual_npp += np.nan_to_num(data)

# 5. Önce 10 ile çarp (10 gün × 36 dekad = yıllık)
annual_npp = annual_npp * 10

# 6. Ardından scale factor uygula (0.001 ile çarp)
annual_npp = annual_npp * 0.001

# 7. Sonucu bir GeoTIFF dosyası olarak kaydet
output_path = os.path.join(folder_path, "Annual_NPP_BE_Lon_WaPOR.tif")

meta.update(dtype=rasterio.float32)

with rasterio.open(output_path, 'w', **meta) as dst:
    dst.write(annual_npp.astype(np.float32), 1)

print("Annual_NPP_Created with Scale Factor:", output_path)
