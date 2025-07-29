import os
import sys
import requests
from pyproj import Transformer
import json  # For PDAL pipeline construction
import subprocess  # For executing PDAL command
from urllib.parse import urlparse  # For parsing URLs
from pathlib import Path
from qgis.core import QgsGeometry, QgsSpatialIndex
import laspy
import numpy as np
from pyproj import CRS, exceptions  # Import CRS from pyproj for checking object type
import argparse

# print("laspy version:", laspy.__version__)
# --- Step 0: Set up the PyQGIS Environment (Crucial for Standalone Scripts) ---
# Check if running in conda environment
if "CONDA_PREFIX" in os.environ:
    QGIS_PATH = os.environ["CONDA_PREFIX"]
    # For conda environments, we need to set these additional paths
    os.environ["GDAL_DATA"] = os.path.join(QGIS_PATH, "share", "gdal")
    os.environ["PROJ_LIB"] = os.path.join(QGIS_PATH, "share", "proj")
else:
    # Fallback to system QGIS path
    QGIS_PATH = "/usr"

# Add QGIS Python paths to system path
os.environ["QGIS_PREFIX_PATH"] = QGIS_PATH
QT_PLUGIN_PATH = os.path.join(QGIS_PATH, "lib", "qt", "plugins")
QGIS_PLUGIN_PATH = os.path.join(QGIS_PATH, "share", "qgis", "python", "plugins")

# Set environment variables
os.environ["QT_PLUGIN_PATH"] = QT_PLUGIN_PATH
os.environ["PYTHONPATH"] = os.pathsep.join(
    [
        os.path.join(QGIS_PATH, "share", "qgis", "python"),
        QGIS_PLUGIN_PATH,
        os.environ.get("PYTHONPATH", ""),
    ]
).strip(os.pathsep)

# Add paths to sys.path if they're not already there
qgis_python_path = os.path.join(QGIS_PATH, "share", "qgis", "python")
if qgis_python_path not in sys.path:
    sys.path.append(qgis_python_path)
if QGIS_PLUGIN_PATH not in sys.path:
    sys.path.append(QGIS_PLUGIN_PATH)

# Print debug information
print("\nQGIS Environment Setup:")
print(f"QGIS_PREFIX_PATH: {os.environ['QGIS_PREFIX_PATH']}")
print(f"QT_PLUGIN_PATH: {os.environ['QT_PLUGIN_PATH']}")
print(f"PYTHONPATH: {os.environ['PYTHONPATH']}")
if "CONDA_PREFIX" in os.environ:
    print(f"GDAL_DATA: {os.environ['GDAL_DATA']}")
    print(f"PROJ_LIB: {os.environ['PROJ_LIB']}")
print(f"sys.path: {sys.path}\n")

try:
    from qgis.core import (
        QgsApplication,
        QgsVectorLayer,
        QgsProject,
        QgsCoordinateReferenceSystem,
        QgsCoordinateTransform,
        QgsPointXY,
        QgsFeatureRequest,
        QgsPoint,
        QgsProviderRegistry,
        QgsDataSourceUri,
    )
except ImportError as e:
    print(f"Error importing PyQGIS modules: {e}")
    print("Please ensure QGIS is installed in your conda environment.")
    print("You can install it using:")
    print("conda install -c conda-forge qgis")
    sys.exit(1)

# Initialize QGIS Application (headless mode - no GUI)
qgs = QgsApplication([], False)
qgs.initQgis()
print("PyQGIS environment initialized for headless operation.")

# --- Define Paths and Constants ---
LIDAR_INDEX_GPKG_PATH = (
    "/home/amadgakkhar/code/qgis-ns-pe/index/Index_LiDARtiles_tuileslidar.gpkg"
)
LIDAR_DIR = Path("lidar_tiles")
OUTPUT_DIR = Path("output")

# Define standard output filenames
SATELLITE_IMAGE = "sat.png"
LIDAR_SUBSET = "lidar_cropped.laz"
BUILDINGS_OUTPUT = "buildings.laz"

# Create directories if they don't exist
os.makedirs(LIDAR_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --- Step 1: Geocode the Address to Lat/Lon ---


def geocode_address(address, user_agent="MyGeocoderApp/1.0 (contact@example.com)"):
    """
    Geocodes a given address using the OpenStreetMap Nominatim API.

    Args:
        address (str): The address to geocode.
        user_agent (str): The User-Agent string including contact info.

    Returns:
        dict: A dictionary with latitude and longitude, or None if not found.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1, "addressdetails": 0}
    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        results = response.json()
        if results:
            return results[0]["lat"], results[0]["lon"]

        else:
            print("No results found for the address.")
            return None, None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error during request: {err}")
    return None, None


# --- Step 2: Convert Lat/Lon to UTM (NAD83(CSRS) / Canada UTM, EPSG:3978) ---
def transform_coords(lat, lon, target_epsg=3978):
    """Transforms WGS84 (Lat/Lon) to a target CRS (e.g., UTM 3978)."""
    transformer = Transformer.from_crs(
        "epsg:4326", f"epsg:{target_epsg}", always_xy=True
    )
    utm_x, utm_y = transformer.transform(
        lon, lat
    )  # pyproj expects (lon, lat) order for transform
    print(f"Transformed to EPSG:{target_epsg}: X={utm_x}, Y={utm_y}")
    return utm_x, utm_y


# --- Step 3: Get Satellite Image (PNG) for the Bounding Box ---


def get_mapbox_static_image(
    lat,
    lon,
    output_path,
    zoom=20,
    width=400,
    height=400,
    access_token="pk.eyJ1Ijoid3VzZWxtYXBzIiwiYSI6ImNqdTVpc2VibDA4c3E0NXFyMmEycHE3dXUifQ.Wy3_Ou1KrVRkIH1UGb_R3Q",
):
    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
        f"{lon},{lat},{zoom}/{width}x{height}?access_token={access_token}"
    )

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        print(f"Satellite map image saved to {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")
        return False


def get_static_map(lat, lon, output_path, zoom=16, width=400, height=400):
    """
    Downloads a static map image from OpenStreetMap's tile-based static map service.

    Args:
        lat (float): Latitude of the center point.
        lon (float): Longitude of the center point.
        output_path (str): File path to save the image.
        zoom (int): Zoom level (default 16).
        width (int): Image width in pixels (max 1280).
        height (int): Image height in pixels (max 1280).

    Returns:
        bool: True if the image was saved successfully, False otherwise.
    """
    base_url = "https://staticmap.openstreetmap.de/staticmap.php"
    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": f"{width}x{height}",
        "maptype": "mapnik",  # or "cycle"
        "markers": f"{lat},{lon},red",
    }

    try:
        response = requests.get(base_url, params=params, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"Invalid content type: {content_type}")
            return False

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        print(f"Map image saved to: {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error fetching map: {e}")
        return False


def get_satellite_image(
    utm_x, utm_y, output_png_path, width=800, height=800, buffer_m=30
):
    """
    Downloads a satellite image from the NRCan map service 'export' endpoint.
    buffer_m: meters to extend bbox from center point for a square image.
    """
    export_base_url = "https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/lidar_point_cloud_canelevation_en/MapServer/export"

    # Define bounding box for the image (e.g., 200m x 200m if buffer_m=100)
    bbox_xmin = utm_x - buffer_m
    bbox_ymin = utm_y - buffer_m
    bbox_xmax = utm_x + buffer_m
    bbox_ymax = utm_y + buffer_m

    bbox_str = f"{bbox_xmin},{bbox_ymin},{bbox_xmax},{bbox_ymax}"

    params = {
        "bbox": bbox_str,
        "bboxSR": 3978,
        "layers": "show:0,1",
        "size": f"{width},{height}",
        "imageSR": 3978,
        "format": "png",
        "transparent": "true",
        "dpi": 96,
        "f": "image",
    }

    try:
        response = requests.get(export_base_url, params=params, stream=True)
        response.raise_for_status()
        print("Requesting:", response.url)

        content_type = response.headers.get("Content-Type", "")
        content_length = int(response.headers.get("Content-Length", 0))

        if "image" not in content_type or content_length == 0:
            print(
                f"Invalid image response. Content-Type: {content_type}, Length: {content_length}"
            )
            return False

        with open(output_png_path, "wb") as out_file:
            bytes_written = 0
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
                bytes_written += len(chunk)

        if bytes_written == 0:
            print("No data written to file. Image is empty.")
            return False

        print(f"Satellite image saved to: {output_png_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error downloading satellite image: {e}")
        return False


# --- Step 4: Find Corresponding LiDAR Tile ---
def find_lidar_tile(utm_x, utm_y, gpkg_path):
    """
    Finds the URL of the LiDAR tile containing the given UTM coordinates.
    """
    if not os.path.exists(gpkg_path):
        print(f"Error: GeoPackage file not found at {gpkg_path}")
        return None

    # Try to open the GeoPackage
    gpkg_layer = QgsVectorLayer(gpkg_path, "GPKG", "ogr")
    if not gpkg_layer.isValid():
        print(f"Error: Unable to open GeoPackage file: {gpkg_path}")
        return None

    # Get the layer name from sublayers
    sublayers = gpkg_layer.dataProvider().subLayers()
    if not sublayers:
        print("No layers found in GeoPackage.")
        return None

    # Get the layer name from the first sublayer
    layer_parts = sublayers[0].split("!!::!!")
    if len(layer_parts) < 2:
        print("Invalid layer format in GeoPackage.")
        return None

    layer_name = layer_parts[1].strip()
    if not layer_name:
        print("Empty layer name found in GeoPackage.")
        return None

    # Load the actual layer
    uri = f"{gpkg_path}|layername={layer_name}"
    lidar_index_layer = QgsVectorLayer(uri, "LiDAR Tiles Index", "ogr")
    if not lidar_index_layer.isValid():
        print("Failed to load LiDAR index layer.")
        return None

    # Create point for spatial query
    query_point = QgsPointXY(utm_x, utm_y)

    # Transform point if needed
    layer_crs = lidar_index_layer.crs()
    if layer_crs.authid() != "EPSG:3978":
        transform = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("EPSG:3978"), layer_crs, QgsProject.instance()
        )
        query_point = transform.transform(query_point)

    # Create point geometry for containment check
    point_geom = QgsGeometry.fromPointXY(query_point)

    # Find intersecting feature
    for feature in lidar_index_layer.getFeatures():
        if feature.geometry().contains(point_geom):
            url = feature["url"]
            if url:
                print(f"Found LiDAR tile URL: {url}")
                return url
            else:
                print("Found matching tile but no URL field.")
                return None

    print("No LiDAR tile found containing the coordinates.")
    return None


# --- New Function: Process LiDAR Subset with laspy ---
def process_lidar_subset_with_laspy(
    input_laz_path, output_laz_path, utm_x, utm_y, buffer_m=25
):
    """
    Subsets a local LAZ point cloud to a 50x50m area around utm_x, utm_y using laspy.
    """
    try:
        print(f"\nReading LAZ file: {input_laz_path}")
        from laspy.compression import LazrsBackend

        with laspy.open(input_laz_path, laz_backend=LazrsBackend()) as fh:
            print("Reading points...")
            las = fh.read()
            print(f"Total points: {len(las.points)}")

            # Get a sample of points to determine coordinate range
            points = np.stack([las.x, las.y, las.z], axis=0).transpose()
            print(f"\nPoint cloud bounds:")
            print(f"X range: [{points[:, 0].min():.2f}, {points[:, 0].max():.2f}]")
            print(f"Y range: [{points[:, 1].min():.2f}, {points[:, 1].max():.2f}]")
            print(f"Target point: X={utm_x:.2f}, Y={utm_y:.2f}")

            # Check if coordinates might be in different CRS
            x_in_range = points[:, 0].min() <= utm_x <= points[:, 0].max()
            y_in_range = points[:, 1].min() <= utm_y <= points[:, 1].max()

            if not (x_in_range and y_in_range):
                print(
                    "\nWarning: Target coordinates appear to be outside point cloud bounds."
                )
                print(
                    "Attempting to transform coordinates from EPSG:3978 to EPSG:2961..."
                )

                # Transform from EPSG:3978 (NAD83 CSRS) to EPSG:2961 (NAD83(CSRS) / MTM zone 5 Nova Scotia)
                transformer = Transformer.from_crs(
                    "EPSG:3978", "EPSG:2961", always_xy=True
                )
                utm_x, utm_y = transformer.transform(utm_x, utm_y)
                print(f"Transformed coordinates: X={utm_x:.2f}, Y={utm_y:.2f}")

            # Define bounds for clipping
            x_min = utm_x - buffer_m
            x_max = utm_x + buffer_m
            y_min = utm_y - buffer_m
            y_max = utm_y + buffer_m

            print(
                f"\nClipping bounds: X[{x_min:.2f}, {x_max:.2f}], Y[{y_min:.2f}, {y_max:.2f}]"
            )

            # Find points within bounds
            mask = (
                (points[:, 0] >= x_min)
                & (points[:, 0] <= x_max)
                & (points[:, 1] >= y_min)
                & (points[:, 1] <= y_max)
            )

            points_in_bounds = mask.sum()
            print(f"Found {points_in_bounds} points within bounds")

            if points_in_bounds == 0:
                # Try with a larger buffer
                print("\nNo points found. Trying with a larger buffer...")
                buffer_m *= 5  # Try 5x larger buffer
                x_min = utm_x - buffer_m
                x_max = utm_x + buffer_m
                y_min = utm_y - buffer_m
                y_max = utm_y + buffer_m

                print(
                    f"New bounds: X[{x_min:.2f}, {x_max:.2f}], Y[{y_min:.2f}, {y_max:.2f}]"
                )

                mask = (
                    (points[:, 0] >= x_min)
                    & (points[:, 0] <= x_max)
                    & (points[:, 1] >= y_min)
                    & (points[:, 1] <= y_max)
                )

                points_in_bounds = mask.sum()
                print(f"Found {points_in_bounds} points with larger buffer")

                if points_in_bounds == 0:
                    print("Still no points found within the specified bounds!")
                    return False

            # Rest of the function remains the same...
            new_header = laspy.LasHeader(
                version=las.header.version, point_format=las.header.point_format
            )
            new_header.offsets = las.header.offsets
            new_header.scales = las.header.scales
            new_header.point_count = points_in_bounds

            print(f"Writing {points_in_bounds} points to output file...")
            with laspy.open(
                output_laz_path, mode="w", header=new_header, laz_backend=LazrsBackend()
            ) as writer:
                new_points = laspy.ScaleAwarePointRecord.zeros(
                    points_in_bounds, header=new_header
                )
                for name in las.point_format.dimension_names:
                    setattr(new_points, name, las[name][mask])
                writer.write_points(new_points)

            print(
                f"Successfully saved subset with {points_in_bounds} points to: {output_laz_path}"
            )
            return True

    except Exception as e:
        print(f"Error processing LAZ file: {str(e)}")
        print("Stack trace:")
        import traceback

        traceback.print_exc()
        return False


def visualize_point_cloud(laz_path, title=None, point_size=0.5, color_by="elevation"):
    """
    Visualizes a LAZ/LAS point cloud in 3D using matplotlib.
    """
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        print(f"Reading point cloud from: {laz_path}")
        with laspy.open(laz_path) as fh:
            las = fh.read()

        # Get points
        points = np.vstack((las.x, las.y, las.z)).transpose()

        # Create figure
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

        # Determine coloring
        if color_by == "elevation":
            colors = points[:, 2]  # Z coordinates
            cmap = plt.cm.viridis
            color_label = "Elevation"
        elif color_by == "intensity" and hasattr(las, "intensity"):
            colors = las.intensity
            cmap = plt.cm.plasma
            color_label = "Intensity"
        elif color_by == "classification" and hasattr(las, "classification"):
            colors = las.classification
            cmap = plt.cm.tab20
            color_label = "Classification"
        else:
            colors = points[:, 2]  # Default to elevation
            cmap = plt.cm.viridis
            color_label = "Elevation"

        # Plot points
        scatter = ax.scatter(
            points[:, 0],
            points[:, 1],
            points[:, 2],
            c=colors,
            cmap=cmap,
            s=point_size,
            alpha=0.6,
        )

        # Add colorbar
        plt.colorbar(scatter, label=color_label)

        # Set labels
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        if title:
            plt.title(title)

        # Make the plot more visually appealing
        ax.grid(True)

        # Set equal aspect ratio
        max_range = (
            np.array(
                [
                    points[:, 0].max() - points[:, 0].min(),
                    points[:, 1].max() - points[:, 1].min(),
                    points[:, 2].max() - points[:, 2].min(),
                ]
            ).max()
            / 2.0
        )

        mean_x = points[:, 0].mean()
        mean_y = points[:, 1].mean()
        mean_z = points[:, 2].mean()

        ax.set_xlim(mean_x - max_range, mean_x + max_range)
        ax.set_ylim(mean_y - max_range, mean_y + max_range)
        ax.set_zlim(mean_z - max_range, mean_z + max_range)

        # Add point count and bounds info
        info_text = f"Total points: {len(points):,}\n"
        info_text += f"X range: [{points[:, 0].min():.2f}, {points[:, 0].max():.2f}]\n"
        info_text += f"Y range: [{points[:, 1].min():.2f}, {points[:, 1].max():.2f}]\n"
        info_text += f"Z range: [{points[:, 2].min():.2f}, {points[:, 2].max():.2f}]"

        plt.figtext(0.02, 0.02, info_text, fontsize=8, family="monospace")

        # Show the plot (but don't save it)
        plt.show()

    except Exception as e:
        print(f"Error visualizing point cloud: {str(e)}")
        import traceback

        traceback.print_exc()


def extract_building_points_laspy(
    input_laz_path, output_building_laz_path, building_class_code=6
):
    """
    Extracts points classified as 'Building' (default Class Code 6) from a LAZ file
    using the laspy library.

    Args:
        input_laz_path (str): Path to the input LAZ/LAS file.
        output_building_laz_path (str): Path where the output LAZ/LAS file
                                        containing only building points will be saved.
        building_class_code (int): The classification code for buildings (default is 6).
    """
    if not os.path.exists(input_laz_path):
        print(f"Error: Input LAZ file not found at {input_laz_path}")
        return False

    print(
        f"\nAttempting to extract building points using laspy from {input_laz_path}..."
    )

    try:
        # Read the LAS/LAZ file
        # laspy.read() returns a LasData object directly, it does not support 'with' statement.
        infile = laspy.read(input_laz_path)

        # Check if 'classification' dimension exists
        if "classification" not in infile.point_format.dimension_names:
            print(
                f"Error: 'classification' dimension not found in {input_laz_path}. Cannot filter by class."
            )
            return False

        # Create a boolean mask for points classified as buildings
        # Standard ASPRS class code for buildings is 6
        building_mask = infile.classification == building_class_code

        # Select the points based on the mask
        out_points = infile.points[building_mask]

        # Create a new LasData object for the filtered points
        # Use infile.header for the header information to ensure compatibility
        outfile = laspy.create(
            point_format=infile.point_format, file_version=infile.header.version
        )
        outfile.points = out_points

        # Write the new LAZ file
        # laspy.LasData.write() handles the file opening/closing internally
        outfile.write(output_building_laz_path)

        print(f"Successfully extracted {len(out_points)} building points.")
        print(f"Building points saved to: {output_building_laz_path}")
        return True

    except Exception as e:
        print(f"An error occurred during laspy processing: {e}")
        return False


def get_laz_crs(laz_file_path):
    """
    Checks and prints the CRS information of a LAZ/LAS file using laspy 2.x.
    """
    if not os.path.exists(laz_file_path):
        print(f"Error: File not found at {laz_file_path}")
        return

    print(f"\nChecking CRS for: {laz_file_path}")
    try:
        with laspy.open(laz_file_path) as fh:
            las = fh.read()
            header = las.header

            # Print coordinate ranges
            print("\nFile coordinate ranges:")
            print(f"X: [{header.x_min:.2f}, {header.x_max:.2f}]")
            print(f"Y: [{header.y_min:.2f}, {header.y_max:.2f}]")
            print(f"Z: [{header.z_min:.2f}, {header.z_max:.2f}]")

            # Check coordinate ranges
            is_pei = (
                300000 <= header.x_min <= 500000 and 600000 <= header.y_min <= 800000
            )

            is_ns = (
                400000 <= header.x_min <= 500000 and 4900000 <= header.y_min <= 5000000
            )

            if is_pei:
                print(
                    "\nCoordinate ranges match PEI Stereographic projection (EPSG:2291)"
                )
                return CRS.from_epsg(2291)
            elif is_ns:
                print("\nCoordinate ranges match Nova Scotia MTM zone 5 (EPSG:2961)")
                return CRS.from_epsg(2961)
            else:
                print(
                    "\nWarning: Could not definitively determine CRS from coordinates"
                )
                print("Coordinates suggest Nova Scotia MTM zone 5 (EPSG:2961)")
                return CRS.from_epsg(2961)

    except Exception as e:
        print(f"Error reading LAZ file: {e}")
        import traceback

        traceback.print_exc()
        return None


# --- Main Script Execution ---
def main(address, index_path, show_3d=False):
    """
    Main function to process LiDAR data for a given address.

    Args:
        address (str): The address to process
        index_path (str): Path to the LiDAR index GPKG file
        show_3d (bool): Whether to show 3D visualizations
    """
    # --- Geocode Address ---
    print(f"\nProcessing address: {address}")
    print(f"Using index file: {index_path}")

    lat, lon = geocode_address(address)
    if lat is None:
        print("Failed to geocode address. Exiting.")
        qgs.exitQgis()
        sys.exit(1)
    print(f"Geocoded address: {lat}, {lon}")

    # --- Transform Coordinates to UTM (EPSG:3978) ---
    utm_x, utm_y = transform_coords(lat, lon, target_epsg=3978)
    print(f"Transformed coordinates: {utm_x}, {utm_y}")

    # --- Get Satellite Image ---
    output_image_path = os.path.join(OUTPUT_DIR, SATELLITE_IMAGE)
    get_mapbox_static_image(lat, lon, output_image_path)

    # --- Find Corresponding LiDAR Tile ---
    lidar_url = find_lidar_tile(utm_x, utm_y, index_path)

    if lidar_url:
        # --- Extract filename from URL and define local path ---
        parsed_url = urlparse(lidar_url)
        laz_filename = os.path.basename(parsed_url.path)
        local_laz_path = os.path.join(LIDAR_DIR, laz_filename)

        # --- Check if LAZ file exists locally ---
        if not os.path.exists(local_laz_path):
            print(f"\nLiDAR file not found in '{LIDAR_DIR}'.")
            print("Please download the file from the following link:")
            print(f"\nDownload Link: {lidar_url}\n")
            print(f"Please save the file to: {LIDAR_DIR}\n")
            input("After downloading the file, press Enter to continue...")

            if not os.path.exists(local_laz_path):
                print("\nError: LiDAR file still not found after download. Exiting.")
                qgs.exitQgis()
                sys.exit(1)

            print("LiDAR file found. Proceeding...")

        # Get CRS info and transform coordinates if needed
        crs_info = get_laz_crs(local_laz_path)

        # --- Process and Save Point Cloud Subset ---
        output_laz_subset_path = os.path.join(OUTPUT_DIR, LIDAR_SUBSET)
        output_buildings_path = os.path.join(OUTPUT_DIR, BUILDINGS_OUTPUT)

        # Transform coordinates based on detected CRS
        if crs_info:
            target_epsg = crs_info.to_epsg()
            if target_epsg == 2961:  # Nova Scotia MTM zone 5
                print(
                    "\nTransforming coordinates to Nova Scotia MTM zone 5 (EPSG:2961)..."
                )
                transformer = Transformer.from_crs(
                    "EPSG:3978", "EPSG:2961", always_xy=True
                )
                utm_x, utm_y = transformer.transform(utm_x, utm_y)
                print(f"Transformed coordinates: X={utm_x:.2f}, Y={utm_y:.2f}")
            elif target_epsg == 2291:  # PEI Stereographic
                print("\nTransforming coordinates to PEI Stereographic (EPSG:2291)...")
                transformer = Transformer.from_crs(
                    "EPSG:3978", "EPSG:2291", always_xy=True
                )
                utm_x, utm_y = transformer.transform(utm_x, utm_y)
                print(f"Transformed coordinates: X={utm_x:.2f}, Y={utm_y:.2f}")
            else:
                print(f"\nUnexpected CRS EPSG:{target_epsg}. Using coordinates as-is.")

        if process_lidar_subset_with_laspy(
            local_laz_path,
            output_laz_subset_path,
            utm_x,
            utm_y,
            buffer_m=20,
        ):
            print(f"\nPoint cloud subset saved to: {output_laz_subset_path}")

            # Extract building points
            if extract_building_points_laspy(
                output_laz_subset_path, output_buildings_path
            ):
                print(f"\nBuilding points saved to: {output_buildings_path}")

            # Only show visualizations if requested
            if show_3d:
                visualize_point_cloud(
                    output_laz_subset_path,
                    title="LiDAR Point Cloud",
                    point_size=1.0,
                    color_by="elevation",
                )
                visualize_point_cloud(
                    output_buildings_path,
                    title="Building Points",
                    point_size=1.0,
                    color_by="elevation",
                )
        else:
            print("\nFailed to process point cloud subset.")
            qgs.exitQgis()
            sys.exit(1)

    else:
        print(
            "\nNo relevant LiDAR tile found for the given address. Cannot subset point cloud."
        )

    # --- Clean up QGIS environment ---
    qgs.exitQgis()
    print("\nScript finished. QGIS environment uninitialized.")
    sys.exit(0)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process LiDAR data for a given address using a LiDAR index file."
    )

    # Required arguments with -- prefix
    parser.add_argument(
        "--address",
        type=str,
        required=True,
        help="Address to process (e.g., '8 Alderwood Dr, Halifax, NS B3N 1S7')",
    )

    parser.add_argument(
        "--index_path",
        type=str,
        required=True,
        help="Path to the LiDAR index GPKG file",
    )

    # Optional arguments
    parser.add_argument(
        "--show_3d",
        action="store_true",
        help="Show 3D visualizations of the point clouds",
    )

    # Parse arguments
    args = parser.parse_args()

    # Create output directories
    os.makedirs(LIDAR_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Run main function with parsed arguments
    main(args.address, args.index_path, args.show_3d)
