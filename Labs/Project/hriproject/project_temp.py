import arcpy
import os

# Paths
input_folder = r"C:\\Users\\gfali\\Desktop\\Cooling_Project\\temp_tif"  # Folder with 48 temperature files
output_folder = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Project"  # Output folder for the raster
gdb_path = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Project\\hriproject\\hriproject.gdb"  # Output geodatabase

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Check if the geodatabase exists
if not arcpy.Exists(gdb_path):
    print(f"Error: Geodatabase not found at {gdb_path}")
else:
    # Collect all Tmax and Tmin TIFF files
    tmin_files = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.tif') and 'tmin' in f])
    tmax_files = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.tif') and 'tmax' in f])

    # Ensure both Tmin and Tmax have 24 files each (2020-2021)
    if len(tmin_files) != 24 or len(tmax_files) != 24:
        print(f"Error: Expected 24 Tmin and 24 Tmax files, but found {len(tmin_files)} Tmin and {len(tmax_files)} Tmax.")
    else:
        # Calculate average for each pair of Tmin and Tmax rasters
        avg_rasters = []
        for tmin_file, tmax_file in zip(tmin_files, tmax_files):
            avg_temp = arcpy.sa.Divide(arcpy.sa.Plus(arcpy.sa.Raster(tmin_file), arcpy.sa.Raster(tmax_file)), 2)
            avg_rasters.append(avg_temp)

        # Calculate the overall average temperature across all 48 months
        overall_avg_temp = arcpy.sa.CellStatistics(avg_rasters, "MEAN", "DATA")

        # Save the overall average temperature raster as a floating-point TIFF
        output_raster = os.path.join(output_folder, "overall_avg_temp_2020_2021.tif")
        overall_avg_temp.save(output_raster)
        print(f"Overall average temperature raster saved as TIFF: {output_raster}")

        # Convert the floating-point raster to an integer raster for RasterToPolygon
        int_raster = arcpy.sa.Int(overall_avg_temp)

        # Save the integer raster to the geodatabase
        int_raster_path = os.path.join(gdb_path, "overall_avg_temp_int")
        int_raster.save(int_raster_path)

        # Convert the integer raster to a polygon feature class in the geodatabase
        output_fc = os.path.join(gdb_path, "overall_avg_temp_polygon")
        arcpy.conversion.RasterToPolygon(int_raster_path, output_fc, "NO_SIMPLIFY", "Value")
        print(f"Overall average temperature raster saved as feature class in geodatabase: {output_fc}")

print("Processing complete!")
