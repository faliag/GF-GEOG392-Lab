import geopandas as gpd
import os
# Construct the file path
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, 'Labs', 'Lab3', 'data.geojson')

# Read the GeoJSON file
gdf = gpd.read_file(file_path)

# Display the first few rows
print(gdf.head())