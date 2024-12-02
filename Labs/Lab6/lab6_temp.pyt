# -*- coding: utf-8 -*-

import arcpy
import time

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Symbology Update Toolbox"
        self.alias = "SymbologyToolbox"
        self.tools = [UpdateSymbology]

class UpdateSymbology(object):
    def __init__(self):
        """Define the tool."""
        self.label = "Update Symbology"
        self.description = "Update symbology for Structures and Trees layers."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions."""
        param_proj_path = arcpy.Parameter(
            displayName="Project File Path",
            name="proj_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Input",
        )
        
        param_layer_name = arcpy.Parameter(
            displayName="Layer Name (Optional)",
            name="layer_name",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
        )
        
        param_output_path = arcpy.Parameter(
            displayName="Output Project Path",
            name="output_proj_path",
            datatype="DEFile",
            parameterType="Optional",
            direction="Output",
        )

        return [param_proj_path, param_layer_name, param_output_path]

    def execute(self, parameters, messages):
        """The source code of the tool."""
        readTime = 3
        start = 0
        max_value = 100
        step = 25

        arcpy.SetProgressor("step", "Initializing tool...", start, max_value, step)

        # Fetch user input
        proj_path = parameters[0].valueAsText
        layer_name = parameters[1].valueAsText
        output_path = parameters[2].valueAsText if parameters[2].valueAsText else proj_path.replace(".aprx", "_updated.aprx")
        
        arcpy.AddMessage("Project path: {}".format(proj_path))
        arcpy.AddMessage("Output project path: {}".format(output_path))
        time.sleep(readTime)

        try:
            arcpy.SetProgressorLabel("Loading project...")
            project = arcpy.mp.ArcGISProject(proj_path)
            time.sleep(readTime)

            # Ensuring that we have a valid map
            maps = project.listMaps('Map')
            if not maps:
                arcpy.AddError("No map found in the project.")
                return

            # Listing layers in the map
            layers = maps[0].listLayers()

            for layer in layers:
                if layer.isFeatureLayer:
                    symbology = layer.symbology
                    
                    if hasattr(symbology, 'renderer') and layer.name == 'Structures':
                        arcpy.SetProgressorPosition(start + step)
                        arcpy.SetProgressorLabel("Updating Structures layer symbology...")
                        symbology.updateRenderer('UniqueValueRenderer')
                        symbology.renderer.fields = ["Type"]
                        layer.symbology = symbology
                        arcpy.AddMessage("Structures layer symbology updated!")
                        time.sleep(readTime)
                    
                    elif hasattr(symbology, 'renderer') and layer.name == 'Trees':
                        arcpy.SetProgressorPosition(start + (2 * step))
                        arcpy.SetProgressorLabel("Updating Trees layer symbology...")
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        symbology.renderer.classificationField = "Shape_Area"
                        symbology.renderer.breakCount = 5
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]
                        layer.symbology = symbology
                        arcpy.AddMessage("Trees layer symbology updated!")
                        time.sleep(readTime)
            
            arcpy.SetProgressorPosition(start + (3 * step))
            arcpy.SetProgressorLabel("Saving updated project...")
            project.saveACopy(output_path)
            arcpy.AddMessage("Project saved at: {}".format(output_path))
            time.sleep(readTime)

            arcpy.SetProgressorPosition(max_value)
            arcpy.SetProgressorLabel("Process completed!")
            arcpy.AddMessage("Symbology update completed successfully!")
            time.sleep(readTime)

        except Exception as e:
            arcpy.AddError("An error occurred: {}".format(str(e)))
            arcpy.SetProgressorPosition(max_value)
            arcpy.SetProgressorLabel("Process failed.")
            time.sleep(readTime)
            return
