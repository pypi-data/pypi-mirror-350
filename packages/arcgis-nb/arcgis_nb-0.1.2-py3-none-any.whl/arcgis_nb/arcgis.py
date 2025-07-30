import requests
import json
from pyproj import Transformer
import math
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os
from pathlib import Path
import numpy as np
import cv2
import laspy
import geopandas as gpd
from shapely.geometry import Point
import sys
import argparse

## Constants
buffer = 30
width = 400
height = 400
format = "png"

DEFAULT_OUTPUT_DIR = Path("output")  # Renamed to avoid conflict
tiles_dir = Path("lidar_tiles")

# Default values for control flags
DEFAULT_VERBOSE = False
DEFAULT_SHOW_3D = False
DEFAULT_POINT_CORRECTION = False


def log(message, verbose=DEFAULT_VERBOSE):
    """
    Print a message if verbose is True.

    Args:
        message: The message to print
        verbose (bool): Whether to print the message
    """
    if verbose:
        print(message)


def display_image(image, title=None, figsize=(8, 8)):
    """
    Display an image - always suppressed in this version.

    Args:
        image: PIL Image or numpy array to display
        title (str, optional): Title for the figure
        figsize (tuple, optional): Figure size
    """
    # Always return without displaying
    return


def get_arcgis_data(address):
    """
    Geocodes an address using GeoNB's ArcGIS REST API and returns coordinates.

    Args:
        address (str): Full address in New Brunswick (e.g., "74 Salisbury Rd Moncton, NB E1E1A4")

    Returns:
        tuple: (X, Y, wgs84_coords) where:
            - X (float): X coordinate in NB Stereographic (EPSG:2036)
            - Y (float): Y coordinate in NB Stereographic (EPSG:2036)
            - wgs84_coords (tuple): (longitude, latitude) in WGS84 (EPSG:4326)

    Raises:
        ValueError: If no results found for the address
        RequestException: If API request fails
        JSONDecodeError: If response parsing fails
    """
    # ArcGIS geocoding service endpoint
    url = "https://geonb.snb.ca/arcgis/rest/services/Geocoding/GeoNB_Composite_Geocoder_SubUnits/GeocodeServer/findAddressCandidates"

    # Request parameters
    params = {"f": "json", "singleLine": address, "outFields": "*"}

    try:
        # Make POST request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Parse JSON response
        result = response.json()

        if not result.get("candidates"):
            raise ValueError(f"No results found for address: {address}")

        if result and result["candidates"]:
            # Get coordinates in New Brunswick Stereographic (EPSG:2036)
            X = result["candidates"][0]["location"]["x"]
            Y = result["candidates"][0]["location"]["y"]

            # print(f"Original coordinates (EPSG:2036): {X}, {Y}")

            # Convert to WGS84 for reference
            wgs84_coords = convert_coordinates(X, Y, from_epsg=2036, to_epsg=4326)
            # print(f"WGS84 coordinates: {wgs84_coords}")

        return X, Y, wgs84_coords

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        return None


def convert_coordinates(x, y, from_epsg=2036, to_epsg=4326):
    """
    Converts coordinates between different coordinate reference systems.

    Args:
        x (float): X coordinate or longitude in source system
        y (float): Y coordinate or latitude in source system
        from_epsg (int, optional): Source coordinate system EPSG code. Defaults to 2036 (NB Stereographic)
        to_epsg (int, optional): Target coordinate system EPSG code. Defaults to 4326 (WGS84)

    Returns:
        tuple: (x, y) coordinates in target coordinate system
    """
    # Create a transformer object
    transformer = Transformer.from_crs(
        f"EPSG:{from_epsg}", f"EPSG:{to_epsg}", always_xy=True
    )

    # Transform the coordinates
    lon, lat = transformer.transform(x, y)

    return lon, lat


def get_geonb_imagery(Y, X, buffer=buffer, width=width, height=height, format=format):
    """
    Retrieves aerial imagery from GeoNB Basemap Imagery service.

    Args:
        Y (float): Y coordinate in NB Stereographic (EPSG:2036)
        X (float): X coordinate in NB Stereographic (EPSG:2036)
        buffer (float, optional): Buffer distance around point in meters. Defaults to 30
        width (int, optional): Image width in pixels. Defaults to 400
        height (int, optional): Image height in pixels. Defaults to 400
        format (str, optional): Image format ('png' or 'jpg'). Defaults to "png"

    Returns:
        PIL.Image: Aerial imagery of the specified location
        None: If request fails
    """

    x, y = X, Y

    url = "https://geonb.snb.ca/arcgis/rest/services/GeoNB_Basemap_Imagery/MapServer/export"

    # Request parameters
    params = {
        "f": "image",
        "format": format,
        "bbox": f"{x-buffer},{y-buffer},{x+buffer},{y+buffer}",
        "bboxSR": 2036,  # New Brunswick Stereographic
        "imageSR": 2036,
        "size": f"{width},{height}",
        "dpi": 96,
        "transparent": "false",
    }

    try:
        # Make GET request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Create image from response
        img = Image.open(BytesIO(response.content))

        # Check if image is empty
        if is_empty_image(img):
            print("Warning: The imagery appears to be empty or blank")

        return img

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


def get_buildings(Y, X, width=width, height=height, buffer=buffer):
    """
    Retrieves building footprint imagery from GeoNB SNB Buildings service.

    Args:
        Y (float): Y coordinate in NB Stereographic (EPSG:2036)
        X (float): X coordinate in NB Stereographic (EPSG:2036)
        width (int, optional): Image width in pixels. Defaults to 400
        height (int, optional): Image height in pixels. Defaults to 400
        buffer (float, optional): Buffer distance around point in meters. Defaults to 30

    Returns:
        PIL.Image: Building footprints image
        None: If request fails or no buildings found
    """
    x, y = X, Y

    url = (
        "https://geonb.snb.ca/arcgis/rest/services/GeoNB_SNB_Buildings/MapServer/export"
    )
    # print(f"{x-buffer},{y-buffer},{x+buffer},{y+buffer}")
    # Request parameters
    params = {
        "f": "image",
        "format": "png",
        "bbox": f"{x-buffer},{y-buffer},{x+buffer},{y+buffer}",
        "bboxSR": 2036,  # New Brunswick Stereographic
        "imageSR": 2036,
        "size": f"{width},{height}",
        "dpi": 96,
        "transparent": "True",
    }

    try:
        # Make GET request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Create image from response
        img = Image.open(BytesIO(response.content))

        # Check if image is empty
        if is_empty_image(img):
            print("Warning: The building footprints image appears to be empty or blank")

        return img

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


def get_lidar_download_info(X, Y):
    """
    Retrieves LiDAR dataset information and download URL for a specific location.

    Args:
        X (float): X coordinate in NB Stereographic (EPSG:2036)
        Y (float): Y coordinate in NB Stereographic (EPSG:2036)

    Returns:
        dict: Dictionary containing LiDAR dataset information including:
            - filename: Name of the LiDAR file
            - year: Year the data was collected
            - point_density: Point density of the LiDAR data
            - vertical_datum: Vertical datum used
            - las_version: LAS file version
            - download_url: URL to download the LAZ file
            - metadata_url: URL to download metadata XML
        None: If no LiDAR data found at location or request fails
    """
    # LiDAR index identify endpoint
    url = "https://geonb.snb.ca/arcgis/rest/services/GeoNB_SNB_LidarIndex/MapServer/identify"

    # Request parameters
    params = {
        "f": "json",
        "geometry": f"{X},{Y}",
        "geometryType": "esriGeometryPoint",
        "tolerance": 10,
        "mapExtent": f"{X-100},{Y-100},{X+100},{Y+100}",
        "imageDisplay": "800,600,96",
        "returnGeometry": "true",
        "layers": "all",
    }

    try:
        # Make GET request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Parse JSON response
        result = response.json()

        if not result.get("results"):
            print("No LiDAR data found at this location")
            return None

        # Extract LiDAR file information
        attributes = result["results"][0]["attributes"]

        lidar_info = {
            "filename": attributes.get("FILENAME"),
            "year": attributes.get("YEAR"),
            "point_density": attributes.get("POINT_DENSITY"),
            "vertical_datum": attributes.get("VERTICAL_DATUM"),
            "las_version": attributes.get("LAS_VERSION"),
            "download_url": attributes.get("FILE_URL"),
        }

        # Add metadata URL if filename exists
        if lidar_info["filename"]:
            metadata_filename = lidar_info["filename"].replace(".laz", "_metadata.xml")
            base_url = "https://geonb.snb.ca/downloads/lidar"
            lidar_info["metadata_url"] = f"{base_url}/{metadata_filename}"

        return lidar_info

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


def is_empty_image(img):
    """
    Checks if an image is effectively empty (transparent or single color).

    Args:
        img (PIL.Image): Image to check

    Returns:
        bool: True if image is empty or single color, False otherwise
    """
    # Convert to RGBA if not already
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Get image data
    data = img.getdata()

    # Check if all pixels are transparent
    if all(pixel[3] == 0 for pixel in data):
        return True

    # Check if all pixels are the same color
    first_pixel = data[0]
    if all(pixel == first_pixel for pixel in data):
        return True

    return False


def pixel_to_geo(px, py, bbox, img_width=width, img_height=height):
    """
    Convert pixel coordinates to geographic coordinates.

    Args:
        px (float): Pixel x-coordinate (column)
        py (float): Pixel y-coordinate (row)
        img_width (int): Width of the image in pixels
        img_height (int): Height of the image in pixels
        bbox (tuple): Bounding box in geographic coordinates (minx, miny, maxx, maxy)

    Returns:
        tuple: (geo_x, geo_y) Geographic coordinates
    """
    minx, miny, maxx, maxy = bbox

    # Calculate the geographic width and height
    geo_width = maxx - minx
    geo_height = maxy - miny

    # Calculate the scaling factors
    x_scale = geo_width / img_width
    y_scale = geo_height / img_height

    # Convert pixel coordinates to geographic coordinates
    # For y-coordinate, we invert because image origin is at top-left
    geo_x = minx + px * x_scale
    geo_y = (
        maxy - py * y_scale
    )  # Subtract from max y because image y increases downward

    return float(geo_x), float(geo_y)


def geo_to_pixel(geo_x, geo_y, bbox, img_width=width, img_height=height):
    """
    Convert geographic coordinates to pixel coordinates.

    Args:
        geo_x (float): Geographic x-coordinate
        geo_y (float): Geographic y-coordinate
        img_width (int): Width of the image in pixels
        img_height (int): Height of the image in pixels
        bbox (tuple): Bounding box in geographic coordinates (minx, miny, maxx, maxy)

    Returns:
        tuple: (px, py) Pixel coordinates
    """
    minx, miny, maxx, maxy = bbox

    # Calculate the geographic width and height
    geo_width = maxx - minx
    geo_height = maxy - miny

    # Calculate the scaling factors
    x_scale = img_width / geo_width
    y_scale = img_height / geo_height

    # Convert geographic coordinates to pixel coordinates
    # For y-coordinate, we invert because image origin is at top-left
    px = (geo_x - minx) * x_scale
    py = (
        maxy - geo_y
    ) * y_scale  # Subtract from max y because image y increases downward

    return px, py


def highlight_closest_polygon_to_center(
    pil_image, X, Y, show=False, verbose=DEFAULT_VERBOSE
):
    """
    Accepts a PIL.Image with transparency, finds the polygon closest to the image center,
    and highlights it by drawing a green outline and a blue center dot.

    Args:
        pil_image (PIL.Image): Input image (must have an alpha channel).
        show (bool): Whether to display the result using matplotlib.

    Returns:
        output_image (np.ndarray): BGR image with the closest polygon highlighted.
        closest_contour (np.ndarray): Contour points of the closest polygon.
        center (tuple): (x, y) coordinates of the image center.
        polygon_centroid (tuple): (x, y) coordinates of the closest polygon's centroid.
    """
    # Ensure image is in RGBA mode
    pil_image = pil_image.convert("RGBA")

    # Convert to NumPy array
    image = np.array(pil_image)

    # Split channels
    bgr = cv2.cvtColor(image[:, :, :3], cv2.COLOR_RGB2BGR)
    alpha = image[:, :, 3]

    # Threshold to isolate non-transparent regions
    _, thresh = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Image center
    h, w = alpha.shape
    center = np.array([w / 2, h / 2])

    # Find contour closest to center
    min_dist = float("inf")
    closest_contour = None
    polygon_centroid = None

    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        dist = np.linalg.norm(center - np.array([cx, cy]))
        if dist < min_dist:
            min_dist = dist
            closest_contour = cnt
            polygon_centroid = (cx, cy)

    # Draw result
    output = bgr.copy()
    if closest_contour is not None:
        cv2.drawContours(output, [closest_contour], -1, (0, 255, 0), 2)
    cv2.circle(output, tuple(center.astype(int)), 5, (255, 0, 0), -1)
    log(f"Polygon centroid {polygon_centroid}", verbose)

    if show:
        display_image(
            cv2.cvtColor(output, cv2.COLOR_BGR2RGB), "Closest Polygon to Center"
        )

    closest_contour_reshaped = np.reshape(closest_contour, (-1, 2))

    geo_points = []
    for point in closest_contour_reshaped:
        geo_point = pixel_to_geo(
            point[0], point[1], (X - buffer, Y - buffer, X + buffer, Y + buffer)
        )
        geo_points.append(geo_point)

    log("Converted Contour Points to Geo Points", verbose)

    return output, geo_points


def clip_lidar_to_contour(
    input_path: str, output_path: str, contour: np.ndarray, buffer_distance: float = 0
):
    """
    Clips a LAZ/LAS file to points that fall within a contour.

    Args:
        input_path (str): Path to input LAZ/LAS file
        output_path (str): Path where the clipped LAZ/LAS file will be saved
        contour (numpy.ndarray): Array of shape (N,2) containing contour points
        buffer_distance (float): Optional buffer distance around contour (in meters)

    Returns:
        str: Path to the clipped file
    """

    # Read the input LAS/LAZ file
    las = laspy.read(input_path)

    # Get point coordinates
    points = np.vstack((las.x, las.y)).transpose()  # Just need x,y for contour check

    # Reshape contour to a format suitable for point-in-polygon test
    # contour = contour.reshape(-1, 2)

    # Apply buffer if requested
    if buffer_distance > 0:
        # Convert contour to a format suitable for cv2.dilate
        contour_img = np.zeros((10000, 10000), dtype=np.uint8)
        # Shift contour to fit within the image bounds
        min_x, min_y = np.min(contour, axis=0)
        shifted_contour = contour - [min_x, min_y] + [500, 500]
        cv2.drawContours(contour_img, [shifted_contour.astype(np.int32)], 0, 255, -1)

        # Create kernel for dilation
        kernel_size = int(buffer_distance)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        # Dilate the contour
        dilated = cv2.dilate(contour_img, kernel, iterations=1)

        # Find contours of the dilated shape
        dilated_contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        buffered_contour = dilated_contours[0].reshape(-1, 2)

        # Shift back to original coordinates
        buffered_contour = buffered_contour + [min_x, min_y] - [500, 500]
        contour = buffered_contour

    # print(contour)
    # print(type(contour))

    # Save contour points to numpy file
    contour_output_path = str(Path(output_path).parent / "contour_points.npy")
    np.save(contour_output_path, contour)
    # Create mask for points within the contour
    mask = np.zeros(len(points), dtype=bool)

    # Check each point if it's inside the contour
    for i, point in enumerate(points):
        # cv2.pointPolygonTest returns positive value if point is inside,
        # negative if outside, and zero if on the edge
        result = cv2.pointPolygonTest(
            contour.astype(np.float32), (float(point[0]), float(point[1])), False
        )
        if result >= 0:  # Point is inside or on the edge
            mask[i] = True

    # Create new LAS file with filtered points
    clipped_las = laspy.create(
        point_format=las.header.point_format, file_version=las.header.version
    )

    # Copy header properties
    clipped_las.header.offsets = las.header.offsets
    clipped_las.header.scales = las.header.scales

    # Copy points within the mask
    for dimension in las.point_format.dimension_names:
        setattr(clipped_las, dimension, las[dimension][mask])

    # Write the clipped data
    clipped_las.write(output_path)

    return output_path


def visualize_laz(laz_path, point_size=0.5, color="blue", alpha=0.6, show=None):
    """
    Visualizes a LAZ/LAS file using Matplotlib in 3D.

    Args:
        laz_path (str): Path to the LAZ/LAS file to visualize
        point_size (float): Size of points in visualization
        color (str): Color of points
        alpha (float): Transparency of points (0-1)
        show (bool): Whether to display the visualization
    """
    if not show:
        return

    # Read the LAZ file
    las = laspy.read(laz_path)

    # Create point cloud from LAZ data
    x = las.x
    y = las.y
    z = las.z

    # Create 3D scatter plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Plot points
    scatter = ax.scatter(x, y, z, c=color, s=point_size, alpha=alpha)

    # Set labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Add a color bar
    plt.colorbar(scatter)

    # Set title
    plt.title("LiDAR Point Cloud Visualization")

    # Show plot
    plt.show()


def visualize_laz_2d(laz_path, point_size=0.5, cmap="terrain", alpha=0.6, show=None):
    """
    Visualizes a LAZ/LAS file as a 2D height map using Matplotlib.

    Args:
        laz_path (str): Path to the LAZ/LAS file to visualize
        point_size (float): Size of points in visualization
        cmap (str): Colormap for height visualization
        alpha (float): Transparency of points (0-1)
        show (bool, optional): Whether to display the visualization. If None, always False.
    """
    # Always return without displaying
    return


def select_point_on_arcgis_image(pil_image):
    """
    Opens an ArcGIS image (400x400) and allows the user to select a single point.
    Returns the coordinates of the selected point and closes the image.

    Args:
        pil_image (PIL.Image): The ArcGIS image to display for point selection

    Returns:
        tuple: (x, y) coordinates of the selected point in image space
    """

    # Convert PIL image to format suitable for matplotlib
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")

    # Create a figure with fixed size
    fig = plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.imshow(pil_image)
    ax.set_title("Click to select a point")
    ax.axis("off")

    # Variable to store the selected point
    selected_point = [None]

    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            selected_point[0] = (x, y)

            # Highlight the selected point
            if hasattr(ax, "point_marker"):
                ax.point_marker.remove()
            ax.point_marker = ax.plot(x, y, "ro", markersize=10)[0]
            fig.canvas.draw()

            # Close the figure after a short delay
            plt.close(fig)

    # Connect the click event
    fig.canvas.mpl_connect("button_press_event", onclick)

    # Show the plot and wait for user interaction
    plt.show(block=True)

    # Return the selected point
    return selected_point[0]


def save_file(file_data, output_path, verbose=DEFAULT_VERBOSE):
    """
    Saves a file to the specified path. Handles different file types including LAZ/LAS and images.

    Args:
        file_data: The data to save. Can be a PIL.Image, laspy.LasData, or file-like object
        output_path (str): Path where the file should be saved

    Returns:
        str: Path to the saved file

    Raises:
        ValueError: If the file type is not supported or cannot be determined
        IOError: If there's an error writing the file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Check file extension
    _, ext = os.path.splitext(output_path)
    ext = ext.lower()

    try:
        # Handle image files
        if ext in [".png", ".jpg", ".jpeg", ".tif", ".tiff"]:
            if isinstance(file_data, Image.Image):
                file_data.save(output_path)
            else:
                raise ValueError(
                    f"Expected PIL.Image for {ext} file, got {type(file_data)}"
                )

        # Handle LAS/LAZ files
        elif ext in [".las", ".laz"]:
            if hasattr(file_data, "write"):  # Check if it's a laspy.LasData object
                file_data.write(output_path)
            else:
                raise ValueError(
                    f"Expected laspy.LasData for {ext} file, got {type(file_data)}"
                )

        # Handle other file types as binary
        else:
            with open(output_path, "wb") as f:
                if hasattr(file_data, "read"):  # File-like object
                    f.write(file_data.read())
                elif isinstance(file_data, bytes):
                    f.write(file_data)
                else:
                    raise ValueError(
                        f"Unsupported data type for {ext} file: {type(file_data)}"
                    )

        log(f"File saved successfully: {output_path}", verbose)
        return output_path

    except Exception as e:
        log(f"Error saving file to {output_path}: {str(e)}", verbose)
        raise


def lidar_tile_exists(file_name, tiles_directory=tiles_dir):
    """
    Checks if a LiDAR tile file exists in the output directory.

    Args:
        file_name (str): Name of the LiDAR tile file
        tiles_directory (str): Directory where the LiDAR tiles are stored
    Returns:
        bool: True if the file exists
    """
    return os.path.exists(os.path.join(tiles_directory, file_name))


def lidar_data_check(X, Y, verbose=DEFAULT_VERBOSE):
    lidar_info = get_lidar_download_info(X, Y)
    lidar_file_name = lidar_info["download_url"].split("/")[-1]
    log("File Name", verbose)

    if lidar_tile_exists(lidar_file_name):
        log("LiDAR Tile Already Exists", verbose)
        return lidar_file_name
    else:
        print("LiDAR Tile Does Not Exist")
        print("Download LiDAR Tile")
        print(lidar_info["download_url"])
        while True:
            print("\nPlease download the LiDAR data from the URL above.")
            print("Type 'proceed' once downloaded, or 'exit' to quit.")
            user_input = input("> ").lower().strip()

            if user_input == "exit":
                log("Exiting program...")
                sys.exit()

            elif user_input == "proceed":
                if lidar_tile_exists(lidar_file_name):
                    print("LiDAR data found successfully!")
                    return lidar_file_name
                else:
                    print("\nLiDAR data still not found in the tiles directory.")
                    print("Please ensure you've downloaded the file to:", tiles_dir)
                    continue

            else:
                print("Invalid input. Please type 'proceed' or 'exit'")
                continue


def main():
    parser = argparse.ArgumentParser(
        description="Tool for extracting and processing LiDAR data for roofing projects. "
        "Takes a New Brunswick address and generates satellite imagery, building footprints, "
        "and clipped LiDAR point clouds."
    )
    parser.add_argument(
        "--address", type=str, required=True, help="New Brunswick address (required)"
    )
    parser.add_argument(
        "--show_3d",
        action="store_true",
        default=DEFAULT_SHOW_3D,
        help=f"Show 3D visualization (default: {DEFAULT_SHOW_3D})",
    )
    parser.add_argument(
        "--no_show_3d",
        action="store_false",
        dest="show_3d",
        help="Disable 3D visualization",
    )
    parser.add_argument(
        "--point_correction",
        action="store_true",
        default=DEFAULT_POINT_CORRECTION,
        help=f"Enable manual point correction (default: {DEFAULT_POINT_CORRECTION})",
    )
    parser.add_argument(
        "--no_point_correction",
        action="store_false",
        dest="point_correction",
        help="Disable manual point correction",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=DEFAULT_VERBOSE,
        help=f"Enable verbose output (default: {DEFAULT_VERBOSE})",
    )
    parser.add_argument(
        "--quiet", action="store_false", dest="verbose", help="Disable verbose output"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Output directory for files (default: {DEFAULT_OUTPUT_DIR})",
    )

    args = parser.parse_args()

    # Set output directory
    output_dir = Path(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    # Set lidar tiles directory
    os.makedirs(tiles_dir, exist_ok=True)

    # Get address from command line or use default
    address = args.address
    if not address:
        address = "71 ANCHORAGE AVENUE, SAINT JOHN, NB E2K5R3"
        log(f"No address provided, using default: {address}", args.verbose)

    log("Getting Co-ordinates from ArcGIS", args.verbose)
    X, Y, wgs84_coords = get_arcgis_data(address)
    log(f"Co-ordinates from ArcGis CRS 2036: {X}, {Y}", args.verbose)

    img1 = get_geonb_imagery(Y, X)
    log("Satellite Image Received", args.verbose)

    if args.point_correction:
        log("Selecting point on image", args.verbose)
        corrected_point = select_point_on_arcgis_image(img1)
        X, Y = pixel_to_geo(
            corrected_point[0],
            corrected_point[1],
            (X - buffer, Y - buffer, X + buffer, Y + buffer),
        )
        log(f"Corrected point: {X}, {Y}", args.verbose)

    img2 = get_buildings(Y, X)
    log("Building Footprint Received", args.verbose)

    cntr_img, geo_points = highlight_closest_polygon_to_center(
        img2, X, Y, show=False, verbose=args.verbose
    )
    log("Highlighted Polygon to Center and received Contour", args.verbose)

    lidar_file_name = lidar_data_check(X, Y, args.verbose)

    # Save contour points to text file

    clip_lidar_to_contour(
        f"{tiles_dir}/{lidar_file_name}",
        f"{output_dir}/{lidar_file_name.replace('.laz', '_clipped.laz')}",
        np.array(geo_points),
        buffer_distance=2,
    )

    save_file(img1, output_dir / "satellite_image.png", args.verbose)
    save_file(img2, output_dir / "building_footprint.png", args.verbose)
    save_file(
        Image.fromarray(cntr_img),
        output_dir / "building_footprint_highlighted.png",
        args.verbose,
    )

    visualize_laz(
        f"{output_dir}/{lidar_file_name.replace('.laz', '_clipped.laz')}",
        point_size=0.5,
        color="blue",
        alpha=0.6,
        show=args.show_3d,
    )


if __name__ == "__main__":
    main()
