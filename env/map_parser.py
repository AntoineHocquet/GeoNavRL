# Map parsing and graph construction
# map_parser.py

import geopandas as gpd
from shapely.geometry import Polygon, Point
import osmnx as ox


def load_geojson(filepath):
    """
    Load a GeoJSON file as a GeoDataFrame.
    Returns walkable area and obstacle polygons separately.
    """
    gdf = gpd.read_file(filepath)
    print(f"🗺️ Loaded {len(gdf)} features from {filepath}")

    walkables = gdf[gdf['type'] == 'walkable']['geometry']
    obstacles = gdf[gdf['type'] == 'obstacle']['geometry']

    return list(walkables), list(obstacles)


def rasterize_geometry(polygons, grid_size):
    """
    Convert polygons into a set of grid (x, y) cells.

    Parameters:
    ----------
    polygons : list of shapely.geometry.Polygon
    grid_size : int

    Returns:
    ----------
    set of (x, y) grid coordinates
    """
    covered = set()

    for x in range(grid_size):
        for y in range(grid_size):
            cell_center = Point(x + 0.5, y + 0.5)
            if any(poly.contains(cell_center) for poly in polygons):
                covered.add((x, y))

    return covered


def load_map(filepath, grid_size=10):
    """
    Load a map file and return a list of obstacle grid cells.

    Returns:
    - walkable_cells : set of (x, y)
    - obstacle_cells : set of (x, y)
    """
    walkables, obstacles = load_geojson(filepath)

    walkable_cells = rasterize_geometry(walkables, grid_size)
    obstacle_cells = rasterize_geometry(obstacles, grid_size)

    return walkable_cells, obstacle_cells



def load_osm_area(place_name, grid_size=20, network_type="walk"):
    """
    Load real-world data from OpenStreetMap.

    Parameters
    ----------
    place_name : str
        Name of the place to search (e.g. "Berlin, Germany").
    grid_size : int
        How many cells per side in rasterization.
    network_type : str
        'walk', 'drive', 'bike', etc.

    Returns
    ----------
    walkable_cells : set of (x, y)
    obstacle_cells : set of (x, y)
    """

    print(f"🌍 Downloading OSM data for '{place_name}'...")

    # Get walking graph + buildings
    G = ox.graph_from_place(place_name, network_type=network_type)
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    buildings = ox.geometries_from_place(place_name, tags={"building": True})

    # Build bounding box grid
    bounds = gdf_edges.total_bounds  # (minx, miny, maxx, maxy)
    minx, miny, maxx, maxy = bounds
    x_step = (maxx - minx) / grid_size
    y_step = (maxy - miny) / grid_size

    walkable_cells = set()
    obstacle_cells = set()

    for i in range(grid_size):
        for j in range(grid_size):
            cell_x = minx + i * x_step + x_step / 2
            cell_y = miny + j * y_step + y_step / 2
            point = Point(cell_x, cell_y)

            # Check if point is near walkable edge
            is_walkable = gdf_edges.distance(point).min() < max(x_step, y_step)
            if is_walkable:
                walkable_cells.add((i, j))

            # Check if point is inside a building
            if any(buildings.contains(point)):
                obstacle_cells.add((i, j))

    return walkable_cells, obstacle_cells
