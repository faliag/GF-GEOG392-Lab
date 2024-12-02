import arcpy

# Path to ArcGIS Pro project
PROJ_PATH = "C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab6\\Lab6.aprx"

# Loading ArcGIS Pro project
project = arcpy.mp.ArcGISProject(PROJ_PATH)

# Accessing first map named "Map"
mapObj = project.listMaps('Map')[0]

# Looping through the layers in the map
for layer in mapObj.listLayers():
    # Checking that the layer is a feature layer
    if layer.isFeatureLayer:
        # Obtaining the symbology object from the layer
        symbology = layer.symbology
        # Making sure the "Structures" layer has a renderer
        if hasattr(symbology, 'renderer') and layer.name == "Structures":
            # Changing the renderer to 'UniqueValueRenderer'
            symbology.updateRenderer('UniqueValueRenderer')
            # Using the 'Type' column as the unique value field
            symbology.renderer.fields = ["Type"]
            # Applying the updated symbology back to the layer
            layer.symbology = symbology
        else:
            print(f"No desired feature class: {layer.name}")
            
# Saving a copy of the updated project
project.saveACopy("C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab6\\Lab6_updated.aprx")
