# test_map_parser.py

import tempfile
import json
from env.map_parser import load_map


def create_temp_geojson():
    """Creates a temporary GeoJSON file with a walkable square and a small obstacle."""
    features = [
        {
            "type": "Feature",
            "properties": {"type": "walkable"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[1, 1], [1, 4], [4, 4], [4, 1], [1, 1]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"type": "obstacle"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[2, 2], [2, 3], [3, 3], [3, 2], [2, 2]]]
            }
        }
    ]

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".geojson", mode="w")
    json.dump(geojson, tmp_file)
    tmp_file.close()
    return tmp_file.name


def test_map_parser_rasterization():
    filepath = create_temp_geojson()
    walkables, obstacles = load_map(filepath, grid_size=5)

    # print for debugging
    print("Walkable cells:", walkables)
    print("Obstacle cells:", obstacles)

    # Obstacle should block (2,2)
    assert (2, 2) in obstacles, "Obstacle cell (2,2) missing"
    assert (2, 2) in walkables, "Obstacle cell should still be within walkable polygon"
    assert len(walkables) > len(obstacles), "Too few walkable cells detected"
