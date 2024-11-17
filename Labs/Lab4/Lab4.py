import arcpy
import os

# Setup base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
arcpy.env.workspace = BASE_DIR

# Define the paths based on your provided details
GDB_Folder = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5"
GDB_Name = "Lab5.gdb"
Garage_CSV_File = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5\\garages.csv"
Garage_Layer_Name = "garages"
Campus_GDB = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5\\Campus.gdb"
Selected_Garage_Name = "Northside Parking Garage"
Buffer_Radius = "150 meters"

# Create GDB if it doesn't exist
GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)
if not arcpy.Exists(GDB_Full_Path):
    arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)

# Load the CSV data into a feature layer
garages = arcpy.management.MakeXYEventLayer(
    Garage_CSV_File,
    "X",  # X coordinate from the CSV
    "Y",  # Y coordinate from the CSV
    Garage_Layer_Name
)

# Check if the garages layer was created successfully
if arcpy.Exists(garages):
    print(f"Garages layer created successfully: {garages}")
else:
    print("Failed to create garages layer.")

# Convert the layer to a feature class and add to the GDB
arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)

# Path to the "Structures" feature class in Campus.gdb
structures = os.path.join(Campus_GDB, "Structures")

# Define the SQL query to select the garage by its name (using LotName here as per your setup)
where_clause = f"LotName = '{Selected_Garage_Name}'"
print(f"Using where_clause: {where_clause}")

# SearchCursor to verify if the garage exists in the LotName field
cursor = arcpy.da.SearchCursor(structures, ["BldgName"], where_clause)
shouldProceed = False
for row in cursor:
    print(f"Checking: {row[0]}")  # Debugging: print each building name
    if row[0].strip().lower() == Selected_Garage_Name.strip().lower():
        shouldProceed = True
        break

# Proceed if the garage exists in the Structures dataset
if shouldProceed:
    # Delete the existing selected garage feature class if it exists
    selected_garage_layer_name = os.path.join(Campus_GDB, "selected_garage")
    if arcpy.Exists(selected_garage_layer_name):
        arcpy.management.Delete(selected_garage_layer_name)
        print(f"Deleted existing selected garage feature class: {selected_garage_layer_name}")

    # Select the garage as a feature layer
    garage_feature = arcpy.analysis.Select(
        garages, selected_garage_layer_name, where_clause
    )

    # Check if the selected garage was saved successfully
    if arcpy.Exists(selected_garage_layer_name):
        print(f"Selected garage saved successfully to: {selected_garage_layer_name}")
    else:
        print(f"Failed to save selected garage to: {selected_garage_layer_name}")

    # Perform buffer operation around the selected garage (150 meters)
    garage_buff_name = os.path.join(GDB_Folder, "buffered_garage")
    arcpy.analysis.Buffer(garage_feature, garage_buff_name, Buffer_Radius)
    print(f"Buffer operation completed: {garage_buff_name}")

    # Perform clip operation (intersect the buffered garage with Structures)
    clip_output = os.path.join(GDB_Folder, "clipped_output")
    arcpy.analysis.Clip(garage_buff_name, structures, clip_output)
    print(f"Clip operation completed: {clip_output}")

    print("Success: The buffer and clip operations completed.")
else:
    print("Error: The specified garage name does not exist in the LotName field.")
