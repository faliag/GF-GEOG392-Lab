import arcpy
import os

# file path to the ArcGIS Pro project
PROJ_PATH = "C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab6\\Lab6.aprx"

# Verifying path
if not os.path.exists(PROJ_PATH):
    print(f"Error: The file at {PROJ_PATH} does not exist or is inaccessible.")
else:
    # Loading the project
    project = arcpy.mp.ArcGISProject(PROJ_PATH)
    print("Project loaded successfully!")

    # Reference the map named "Map"
    mapObj = project.listMaps('Map')[0]

    # Path to the Campus.gdb
    gdb_path = "C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab6\\Campus.gdb"

    # Referencing Trees feature layer in geodatabase
    trees_layer = f"{gdb_path}\\Trees"

    # Adding the Trees layer to the map
    arcpy.management.MakeFeatureLayer(trees_layer, "Trees_Layer")
    mapObj.addDataFromPath(trees_layer)

    # Looping through the layers to configure symbology for the "Trees" layer
    for layer in mapObj.listLayers():
        if layer.isFeatureLayer and layer.name == "Trees":
            # Getting the symbology object
            symbology = layer.symbology

            # Changing the renderer to 'GraduatedColorsRenderer'
            symbology.updateRenderer('GraduatedColorsRenderer')

            # Setting classification field to Shape_Area
            symbology.renderer.classificationField = "Shape_Area"

            # Setting number of classes (bins) to 5
            symbology.renderer.breakCount = 5

            # Setting color ramp to 'Oranges (5 Classes)'
            symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

            # Applying the updated symbology to the layer
            layer.symbology = symbology

    # Saving the project with changes
    project.save()

    # saving an additional copy to prevent overwriting
    project.saveACopy("C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab6\\Lab6_new.aprx")

    print("Choropleth map created and project saved successfully!")
