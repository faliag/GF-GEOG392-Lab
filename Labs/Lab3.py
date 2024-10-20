import geopandas as gpd
import os

# Constructing the file path
file_path = os.path.join(os.path.dirname(__file__), '..', 'Labs', 'data.geojson')

# Reading the GeoJSON file
gdf = gpd.read_file(file_path)

# Displaying the first few rows
print(gdf.head())

from shapely.geometry import Polygon

class CensusTract:
    def __init__(self, GeoId, Pop, geometry):
        self.geoid = GeoId
        self.population = Pop
        self.geometry = geometry

    def calculate_population_density(self):
        if self.geometry.is_valid and self.geometry.area > 0:
            return self.population / self.geometry.area  # People per square meter
        return None



# Calculate population density and add it directly to a new column in gdf
gdf['pop_den_new'] = gdf.apply(
    lambda row: CensusTract(row['GeoId'], row['Pop'], row['geometry']).calculate_population_density(), axis=1
)

# Display the result
print(gdf)
print(gdf.crs) 