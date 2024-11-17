import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the workspace to the base directory where the script is located
arcpy.env.workspace = BASE_DIR

# Set paths
GDB_Folder = "C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5"
GDB_Name = "Lab5.gdb"
Garage_CSV_File = "C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5\\garages.csv"
Garage_Layer_Name = "garages"
Campus_GDB = "C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5\\Campus.gdb"
Selected_Garage_Name = "Northside Parking Garage"  # The garage name you're searching for
Buffer_Radius = "150 meter"

# Create the file geodatabase
arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)
GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)

# Import the garage data from CSV using X and Y columns
garages = arcpy.management.MakeXYEventLayer(
    Garage_CSV_File, "X", "Y", Garage_Layer_Name
)
arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)

# Creating search cursor to find the selected garage in the Campus GDB
structures = Campus_GDB + "\\Structures"
where_clause = "BldgName = '{}'".format(Selected_Garage_Name)  # Searching by BldgName

# Checking selected garage in the Structures feature class
cursor = arcpy.da.SearchCursor(structures, ["BldgName"], where_clause=where_clause)

shouldProceed = False

for row in cursor:
    if Selected_Garage_Name in row:
        shouldProceed = True
        break

if shouldProceed:
    # Selecting the garage as feature layer
    selected_garage_layer_name = "selected_garage"
    arcpy.management.MakeFeatureLayer(structures, selected_garage_layer_name, where_clause)
    
    # Performing Buffer analysis
    garage_buff_name = os.path.join(GDB_Full_Path, "building_buffed")
    arcpy.analysis.Buffer(selected_garage_layer_name, garage_buff_name, Buffer_Radius)

    # Clip buffered area with the campus structure layer
    clipped_output = os.path.join(GDB_Full_Path, "clipped_garage")
    arcpy.analysis.Clip(garage_buff_name, structures, clipped_output)

    print("Success: Buffer and clip operations completed.")
else:
    print("Error: Garage not found.")
