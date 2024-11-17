# -*- coding: utf-8 -*-

import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Lab5_Toolbox"
        self.alias = "Lab5_Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Lab5_Tool]

class Lab5_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5_Tool"
        self.description = "Tool to process garages and perform spatial analysis (Buffer & Clip)."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions."""
        param_GDB_folder = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdbfolder",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_GDB_Name = arcpy.Parameter(
            displayName="GDB Name",
            name="gdbname",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Garage_CSV_File = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garage_csv",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param_Garage_Layer_Name = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="garage_layer_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Campus_GDB = arcpy.Parameter(
            displayName="Campus Geodatabase",
            name="campus_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        param_Selected_Garage_Name = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="selected_garage",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_Buffer_Radius = arcpy.Parameter(
            displayName="Buffer Radius",
            name="buffer_radius",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        # Add parameters to a list
        params = [
            param_GDB_folder,
            param_GDB_Name,
            param_Garage_CSV_File,
            param_Garage_Layer_Name,
            param_Campus_GDB,
            param_Selected_Garage_Name,
            param_Buffer_Radius
        ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal validation."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Query user input
        GDB_Folder = parameters[0].valueAsText
        GDB_Name = parameters[1].valueAsText
        Garage_CSV_File = parameters[2].valueAsText
        Garage_Layer_Name = parameters[3].valueAsText
        Campus_GDB = parameters[4].valueAsText
        Selected_Garage_Name = parameters[5].valueAsText
        Buffer_Radius = parameters[6].valueAsText

        arcpy.AddMessage("User Input:")
        arcpy.AddMessage(f"GDBFolder: {GDB_Folder}")
        arcpy.AddMessage(f"GDB_Name: {GDB_Name}")
        arcpy.AddMessage(f"Garage_CSV_File: {Garage_CSV_File}")
        arcpy.AddMessage(f"Garage_Layer_Name: {Garage_Layer_Name}")
        arcpy.AddMessage(f"Campus_GDB: {Campus_GDB}")
        arcpy.AddMessage(f"Selected_Garage_Name: {Selected_Garage_Name}")
        arcpy.AddMessage(f"Buffer_Radius: {Buffer_Radius}")

        # path
        GDB_Folder = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5"
        Campus_GDB = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5\\Campus.gdb"
        Garage_CSV_File = r"C:\\Users\\gfali\\.ssh\\GF-GEOG392-Lab\\Labs\\Lab5\\garages.csv"
        GDB_Name = "Lab5.gdb"  # You can also set this dynamically if needed.

        # Create the output GDB if non-existing
        GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)
        if not arcpy.Exists(GDB_Full_Path):
            arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)

        # Import garage CSV and create XY layer
        garages = arcpy.management.MakeXYEventLayer(Garage_CSV_File, "X", "Y", Garage_Layer_Name)
        arcpy.FeatureClassToGeodatabase_conversion(garages, GDB_Full_Path)

        # Search for selected garage in Structures feature class
        structures = os.path.join(Campus_GDB, "Structures")
        where_clause = f"BldgName = '{Selected_Garage_Name}'"
        cursor = arcpy.da.SearchCursor(structures, ["BldgName"], where_clause)

        shouldProceed = False

        for row in cursor:
            if row[0] == Selected_Garage_Name:
                shouldProceed = True
                break

        if shouldProceed:
            # Select the garage as feature layer
            selected_garage_layer_name = "selected_garage"
            arcpy.management.MakeFeatureLayer(structures, selected_garage_layer_name, where_clause)

            # Buffer the selected building
            garage_buff_name = os.path.join(GDB_Full_Path, "building_buffed")
            arcpy.analysis.Buffer(selected_garage_layer_name, garage_buff_name, Buffer_Radius)

            # Clip the buffered feature with the Structures layer
            clipped_output = os.path.join(GDB_Full_Path, "clipped_garage")
            arcpy.analysis.Clip(garage_buff_name, structures, clipped_output)

            arcpy.AddMessage("Success: Buffer and clip operations completed.")
        else:
            arcpy.AddError(f"Error: Garage '{Selected_Garage_Name}' not found in the Structures.")

        return
