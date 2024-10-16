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
    def __init__(self, geoid, population, geometry):
        self.geoid = geoid
        self.population = population
        self.geometry = geometry
    
    def calculate_population_density(self):
        # Calculating the area of the geometry in square kilometers
        area_km2 = self.geometry.area / 1e6  # Convert from square meters to square kilometers
        
        # Calculating the population density
        population_density = self.population / area_km2
        
        return population_density
#'gdf' is the GeoDataFrame:
# example of the instantiation for the first row of this GeoDataFrame
first_tract = CensusTract(
    geoid=gdf.loc[0, 'GeoId'],
    population=gdf.loc[0, 'Pop'],
    geometry=gdf.loc[0, 'geometry']
)
# Accessing attributes of this instantiated object:
print(f"GeoId: {first_tract.geoid}")
print(f"Pop: {first_tract.population}")
print(f"geometry: {first_tract.geometry}")

# Iterating through the GeoDataFrame to create instances for all rows:
census_tracts = []
for index, row in gdf.iterrows():
    tract = CensusTract(row['GeoId'], row['Pop'], row['geometry'])
    census_tracts.append(tract)

# List of CensusTract objects called 'census_tracts':
for tract in census_tracts:
    print(f"Geoid: {tract.geoid}, Population: {tract.population}")


# Calculating density (assuming 'Pop' is population and 'ALAND' is land area)
gdf['population_density'] = gdf['Pop'] / gdf['ALAND']

#Printing the density column:
print(gdf['population_density'])

print(gdf)