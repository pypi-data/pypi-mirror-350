import geojson

def load_geojson(file_path: str) -> dict:
    with open(file_path, "r") as f:
        geojson_data = geojson.load(f)
    return geojson_data
