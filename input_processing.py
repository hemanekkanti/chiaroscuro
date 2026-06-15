import numpy as np
import rasterio
from rasterio.enums import Resampling
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from scipy.ndimage import gaussian_filter


def load_dem(path: str) -> tuple[np.ndarray, dict]:
    """Load any rasterio-readable DEM (GeoTIFF, NetCDF, ASCII grid, etc.)."""
    with rasterio.open(path) as src:
        dem = src.read(1).astype(np.float64)
        meta = {
            "crs": src.crs,
            "transform": src.transform,
            "res": src.res,          # (x_res, y_res) in map units
            "nodata": src.nodata,
        }
    # Mask nodata
    if meta["nodata"] is not None:
        dem[dem == meta["nodata"]] = np.nan
    return dem, meta