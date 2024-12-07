import arcpy
from arcpy.sa import Raster

# Setting up the base directory and workspace
base_dir = "C:\\Users\\gfali\\Downloads\\Lab7Data\\LandSAT"
output_gdb = "C:\\Users\\gfali\\Downloads\\Lab7Data\\lab7data\\lab7data.gdb"
arcpy.env.workspace = output_gdb
arcpy.CheckOutExtension("Spatial")

# Inputting the band paths from te LandSAT folder
band_red_path = f"{base_dir}\\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B3.TIF"  # RED
band_green_path = f"{base_dir}\\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B2.TIF"  # GREEN
band_blue_path = f"{base_dir}\\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B1.TIF"  # BLUE
band_nir_path = f"{base_dir}\\LT05_L2SP_026039_20110803_20200820_02_T1_SR_B4.TIF"  # NIR

# Output paths
output_composite = f"{output_gdb}\\RGB_Composite"
output_ndvi = f"{output_gdb}\\NDVI"

#Creating the RGB Composite Image
print("Creating RGB Composite Image...")
arcpy.management.CompositeBands(
    [band_red_path, band_green_path, band_blue_path],
    output_composite
)
print(f"Composite Image created at: {output_composite}")

#Calculating NDVI
print("Calculating NDVI...")
band_red = Raster(band_red_path)
band_nir = Raster(band_nir_path)

# Using the NDVI formula: ((NIR - RED) / (NIR + RED)) * 100 + 100
ndvi = ((band_nir - band_red) / (band_nir + band_red)) * 100 + 100

# Saving NDVI raster
ndvi.save(output_ndvi)
print(f"NDVI raster created at: {output_ndvi}")

# Checking in the Spatial Analyst extension
arcpy.CheckInExtension("Spatial")

print("Processing completed!")
