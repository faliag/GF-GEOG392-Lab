import arcpy
import os

# Setup base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

### Input paths
INPUT_DB_PATH = r"C:\Users\gfali\.ssh\GF-GEOG392-Lab\Labs\Lab4\Lab4_Data\Campus.gdb"
CSV_PATH = r"C:\Users\gfali\.ssh\GF-GEOG392-Lab\Labs\Lab4\Lab4_Data\garages.csv"
OUTPUT_DB_PATH = r"C:\Users\gfali\.ssh\GF-GEOG392-Lab\Labs\Lab4\Lab4_Data\Lab4.gdb"

# Set the workspace to the input GDB
arcpy.env.workspace = INPUT_DB_PATH

# Layers need to be kept
layers_to_keep = ["GaragePoints", "LandUse", "Structures", "Trees"]

# List all feature classes
feature_classes = arcpy.ListFeatureClasses()

# Delete other classes not in layers_to_keep
for fc in feature_classes:
    if fc not in layers_to_keep:
        arcpy.management.Delete(fc)

# Create output GDB if it doesn't exist: Created earlier as Lab4.gdb
if not os.path.exists(OUTPUT_DB_PATH):
    arcpy.management.CreateFileGDB(os.path.dirname(OUTPUT_DB_PATH), os.path.basename(OUTPUT_DB_PATH))

# Loading the .csv file to input GDB as a Point Feature Layer
garage_points_layer = "GaragePoints"
if not arcpy.Exists(garage_points_layer):
    arcpy.management.XYTableToPoint(CSV_PATH, os.path.join(INPUT_DB_PATH, garage_points_layer), "Longitude", "Latitude")

# Print spatial references
print(f"Before Buffer and Intersect...")
print(f"GaragePoints layer spatial reference: {arcpy.Describe(garage_points_layer).spatialReference.name}.")
print(f"Structures layer spatial reference: {arcpy.Describe('Structures').spatialReference.name}.")

# As we can see that the spatial references match, no need to re-project. Continuing to buffer and intersect.

# Buffer analysis around garages (150 meters)
buffer_output = os.path.join(OUTPUT_DB_PATH, "GarageBuffer")
arcpy.analysis.Buffer(garage_points_layer, buffer_output, "150 meters")

# Intersect analysis (between buffer & Structures)
intersect_output = os.path.join(OUTPUT_DB_PATH, "Garage_Structures_Intersect")
arcpy.analysis.Intersect([buffer_output, "Structures"], intersect_output)

# Output final layers to the geodatabase, Lab4.gdb
arcpy.management.CopyFeatures(garage_points_layer, os.path.join(OUTPUT_DB_PATH, "FinalGaragePoints"))
arcpy.management.CopyFeatures("Structures", os.path.join(OUTPUT_DB_PATH, "FinalStructures"))
arcpy.management.CopyFeatures(buffer_output, os.path.join(OUTPUT_DB_PATH, "FinalGarageBuffer"))
arcpy.management.CopyFeatures(intersect_output, os.path.join(OUTPUT_DB_PATH, "FinalIntersectedStructures"))

#If everthing works well, the output will say:
print("It Works!")
