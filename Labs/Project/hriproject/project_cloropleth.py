import arcpy

# Paths to geodatabase and layers
gdb_path = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Project\\hriproject\\hriproject.gdb"
county_layer = f"{gdb_path}\\tx_projected"  # Updated polygon layer name
hridata_points_layer = f"{gdb_path}\\hridata_points"  # Updated point layer name
output_layer = f"{gdb_path}\\county_hri_choropleth"

# Set workspace
arcpy.env.workspace = gdb_path

# Debug: Print feature classes in geodatabase
print("Available feature classes:", arcpy.ListFeatureClasses())

# Spatial join: aggregate point data into county polygons
output_join = f"{gdb_path}\\county_hri_join"
arcpy.analysis.SpatialJoin(
    target_features=county_layer,
    join_features=hridata_points_layer,
    out_feature_class=output_join,
    join_type="KEEP_ALL",
    match_option="INTERSECT",
    field_mapping=""
)

# Optional: Rename the aggregated count field for clarity
arcpy.management.AlterField(
    in_table=output_join,
    field="Join_Count",  # Default field created for count in Spatial Join
    new_field_name="HRI_Count",
    new_field_alias="HRI Count"
)

# Save the final output as a new layer
arcpy.management.CopyFeatures(output_join, output_layer)

print("Choropleth map created successfully! The output is located at:", output_layer)
