import arcpy

# Setting my workspace and input the DEM
workspace = "C:\\Users\\gfali\\Downloads\\Lab7Data"
arcpy.env.workspace = workspace

# DEM file
input_dem = "C:\\Users\\gfali\\Downloads\\Lab7Data\\DEM\\n30_w097_1arc_v3.tif"

# GDB for outputs
output_gdb = "C:\\Users\\gfali\\Downloads\\Lab7Data\\lab7data\\lab7data.gdb"

# Output within GDB
output_hillshade = f"{output_gdb}\\hillshade"
output_slope = f"{output_gdb}\\slope"

# HillShade param
azimuth = 315  # Default azimuth
altitude = 45  # Default altitude
shadows = "NO_SHADOWS"  # No shadows
z_factor_hillshade = 1  # Default Z factor

# Generate HillShade
print("Generating HillShade raster...")
arcpy.ddd.HillShade(
    input_dem,
    output_hillshade,
    azimuth,
    altitude,
    shadows,
    z_factor_hillshade
)
print(f"HillShade raster created in geodatabase at: {output_hillshade}")

# Slope param
measurement = "DEGREE"  # Default measurement
z_factor_slope = 1  # Default Z factor

# Generate Slope
print("Generating Slope raster...")
arcpy.ddd.Slope(
    input_dem,
    output_slope,
    measurement,
    z_factor_slope
)
print(f"Slope raster created in geodatabase at: {output_slope}")
