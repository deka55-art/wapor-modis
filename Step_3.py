import rasterio
from rasterio.warp import reproject, Resampling

# Ref raster: WaPOR
wapor_path = "C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_WaPOR/Annual_NPP_BE_Lon_WaPOR.tif"
modis_path = "C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_MODIS17/converted_MOD17_BE_Lon.tif"

modis_out_path = r"C:/Users/Casper/Desktop/Kişisel/Kaan/Article/Shapefiles/BE_Lon_MODIS17/aligned_MOD17_BE_Lon_Modis.tif"

# Get WaPOR Coordinate info
with rasterio.open(wapor_path) as ref:
    dst_crs = ref.crs
    dst_transform = ref.transform
    dst_width = ref.width
    dst_height = ref.height

# Read MODIS
with rasterio.open(modis_path) as src:
    modis_data = src.read(1)
    profile = src.profile.copy()
    profile.update({
        'crs': dst_crs,
        'transform': dst_transform,
        'width': dst_width,
        'height': dst_height
    })

    with rasterio.open(modis_out_path, 'w', **profile) as dst:
        reproject(
            source=modis_data,
            destination=rasterio.band(dst, 1),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )
