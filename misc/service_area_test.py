import arcpy

with open("password.txt", 'r') as pw_file:
    pw = pw_file.read()

arcpy.SignInToPortal("https://www.arcgis.com/", "gpaiement_intern_hackathon", pw)

# Instantiate a ServiceArea analysis object.
service_area = arcpy.nax.ServiceArea("https://www.arcgis.com/")


# Get the desired travel mode for the analysis.
nd_layer_name = "https://www.arcgis.com/"
nd_travel_modes = arcpy.nax.GetTravelModes(nd_layer_name)
travel_mode = nd_travel_modes["Walking Time"]

# Set properties.
service_area.timeUnits = arcpy.nax.TimeUnits.Minutes
service_area.defaultImpedanceCutoffs = [20]
service_area.travelMode = travel_mode
service_area.outputType = arcpy.nax.ServiceAreaOutputType.Polygons
service_area.geometryAtOverlap = arcpy.nax.ServiceAreaOverlapGeometry.Split


service_area.load(arcpy.nax.ServiceAreaInputDataType.Facilities, r"C:\Users\gre13341\Documents\Hackathon\New_File_Geodatabase.gdb\single_house")

result = service_area.solve()

output_type = arcpy.nax.ServiceAreaOutputType.Polygons
result.export(output_type, r"C:\Users\gre13341\Documents\Hackathon\New_File_Geodatabase.gdb\polygon")