import arcpy
import os
import pandas as pd

# Set workspace
workspace = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\hriprojectgeog"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

# Define the paths to the input data
csv_path = os.path.join(workspace, "hridata.csv")
shapefile_path = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\hriprojectgeog\\tx.shp"
gdb_path = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\hriprojectgeog\\hriprojgeog\\hriprojgeog.gdb"
aprx_path = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\hriprojectgeog\\hriprojgeog\\hriprojgeog.aprx"

# Spatial Reference (WGS 1984)
spatial_ref = arcpy.SpatialReference(4326)  # WGS 1984

# Diagnose the CSV
print("CSV Diagnostics:")
try:
    df = pd.read_csv(csv_path)
    print("CSV columns:", list(df.columns))
    print("\nFirst few rows:")
    print(df.head())
    print("\nSpecific columns of interest:")
    print("X column (DisplayX):", df['DisplayX'].describe())
    print("Y column (DisplayY):", df['DisplayY'].describe())
except Exception as e:
    print(f"Error reading CSV: {e}")

# Convert CSV to table
csv_table = os.path.join(gdb_path, "hridata_table")
arcpy.TableToTable_conversion(csv_path, gdb_path, "hridata_table")
print(f"\nCSV converted to table: {csv_table}")

# Create point feature class using DisplayX and DisplayY
output_fc = os.path.join(gdb_path, "hridata_points")
arcpy.management.XYTableToPoint(csv_table, output_fc, "DisplayX", "DisplayY", coordinate_system=spatial_ref)
print(f"Point feature class created: {output_fc}")

try:
    # Define projections for input layers
    arcpy.management.DefineProjection(output_fc, spatial_ref)
    arcpy.management.DefineProjection(shapefile_path, spatial_ref)
    
    # Project the county shapefile
    projected_county_shp = os.path.join(gdb_path, "tx_projected")
    arcpy.management.Project(shapefile_path, projected_county_shp, spatial_ref)
    
    # Load the ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    map_obj = aprx.listMaps()[0]
    
    # Remove existing layers
    for layer in map_obj.listLayers():
        map_obj.removeLayer(layer)
    
    # Add layers from paths
    output_layer = arcpy.MakeFeatureLayer_management(output_fc, "hridata_points_layer")
    county_layer = arcpy.MakeFeatureLayer_management(projected_county_shp, "county_layer")
    map_obj.addLayer(output_layer[0])
    map_obj.addLayer(county_layer[0])
    
    print("\nLayers added successfully.")
    
    # Save the project
    aprx.save()
    print("Project saved successfully.")
    
    # Verify coordinate systems
    desc_points = arcpy.Describe(output_fc)
    desc_counties = arcpy.Describe(projected_county_shp)
    print(f"\nPoint Feature Class Coordinate System: {desc_points.spatialReference.name}")
    print(f"County Shapefile Coordinate System: {desc_counties.spatialReference.name}")
    print(f"\nPoint Feature Class Extent: {desc_points.extent}")
    print(f"County Shapefile Extent: {desc_counties.extent}")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    import traceback
    traceback.print_exc()
