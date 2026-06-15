import time
import numpy as np
import rasterio
from scipy.ndimage import sobel
import matplotlib.pyplot as plt

def generate_dufour_shading(geotiff_path, output_path, hachure_frequency=0.4, ink_thickness=3.0):
    start = time.time()
    # read the raw elevation dataset
    with rasterio.open(geotiff_path) as src:
        # read the first band (elevation data)
        elevation = src.read(1).astype(float)
        # get spatial resolution (pixel size in meters)
        dx_meters, dy_meters = src.res

    # compute analytical gradients using Sobel filters
    # we divide by 8.0 to normalize the standard 3x3 Sobel kernel weight
    dz_dx = sobel(elevation, axis=1) / (8.0 * dx_meters)
    dz_dy = sobel(elevation, axis=0) / (8.0 * dy_meters)

    # derive surface normal vectors (Nx, Ny, Nz)
    # the normal vector points perpendicular to the terrain surface slope
    normal_x = -dz_dx
    normal_y = -dz_dy
    normal_z = np.ones_like(elevation)

    # normalize the vectors to unit length
    magnitude = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
    nx = normal_x / magnitude
    ny = normal_y / magnitude
    nz = normal_z / magnitude

    # Define Dufour Northwest light vector (pointing from Top-Left, 45 degrees up)
    light_dir = np.array([-1.0, 1.0, 0.5])
    light_dir /= np.linalg.norm(light_dir)

    # Calculate Lambertian Diffuse Lighting
    # dot product between surface normal and light direction
    dot_nl = (nx * light_dir[0]) + (ny * light_dir[1]) + (nz * light_dir[2])
    diffuse = np.clip((dot_nl + 1.0) * 0.5, 0.0, 1.0)

    # Calculate Slope Steepness
    # As the terrain gets steeper, nz approaches 0.0
    steepness = 1.0 - np.clip(nz, 0.0, 1.0)

    # Generate a 45-degree Screen-Space Hatching Pattern
    # Create coordinate meshes matching the data grid dimensions
    rows, cols = elevation.shape
    y_indices, x_indices = np.indices((rows, cols))

    # Creating a repeating sine wave running diagonally across the matrix array
    diagonal_grid = (x_indices + y_indices) * hachure_frequency
    line_pattern = (np.sin(diagonal_grid) + 1.0) * 0.5

    # Calculate dynamic line dilation weights
    shadow_weight = 1.0 - diffuse
    target_thickness = np.clip(shadow_weight * steepness * ink_thickness, 0.0, 0.95)

    # Apply the binary ink deposition threshold (the step function)
    ink_mask = line_pattern < target_thickness

    # Create the final canvas composition (Vintage Paper background, Dark Iron Gall Ink)
    paper_color = np.array([245, 240, 227]) / 255.0
    ink_color = np.array([20, 20, 30]) / 255.0

    # Broadcast colors across 3 channels (RGB)
    final_image = np.zeros((rows, cols, 3))
    for i in range(3):
        final_image[:, :, i] = np.where(ink_mask, ink_color[i], paper_color[i])

    # Save and export the final map layout
    plt.figure(figsize=(12, 12), dpi=300)
    plt.imshow(final_image)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    end = time.time()
    print(f"Successfully compiled Dufour render and saved to: {output_path} in {end - start:.2f} seconds")

# Example Execution:
# gather up your data into a stitched master file first using the merge_datasets.py script,
# then run this to generate the Dufour-style shaded relief map
generate_dufour_shading("test_chunks_data_io/swissalti3d_stitched_master.tif", "test_chunks_data_io/test_dufour_output_34_chunks.png")
