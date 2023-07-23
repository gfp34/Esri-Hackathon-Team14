import arcpy
import uuid

class ServiceArea:
    def __init__(self):
        arcpy.env.overwriteOutput = True

        #TODO: Change this path depending on user running the backend
        nd_path = r"C:\Users\gre13341\Documents\Hackathon\NorthAmerica\NorthAmerica.gdb\Routing\Routing_ND"
        self.nd_layer_name = "NorthAmerica"

        # Create a network dataset layer. The layer will be referenced using its name.
        arcpy.nax.MakeNetworkDatasetLayer(nd_path, self.nd_layer_name)

        # Instantiate a ServiceArea analysis object.
        self.service_area = arcpy.nax.ServiceArea(self.nd_layer_name)

    def set_properties(self, travel_mode, cutoff_list):
        # Get the desired travel mode for the analysis.
        nd_travel_modes = arcpy.nax.GetTravelModes(self.nd_layer_name)
        if travel_mode == "walking":
            travel_mode = nd_travel_modes["Walking Time"]
        elif travel_mode == "driving":
            travel_mode = nd_travel_modes["Driving Time"]
        else:
            raise ValueError("Invalid travel_mode")
        
        if not isinstance(cutoff_list, list):
            for val in cutoff_list:
                if not isinstance(val, int) or val < 0:
                    raise ValueError("Invalid cutoff_list")

        # Set properties
        self.service_area.timeUnits = arcpy.nax.TimeUnits.Minutes
        self.service_area.defaultImpedanceCutoffs = cutoff_list
        self.service_area.travelMode = travel_mode
        self.service_area.outputType = arcpy.nax.ServiceAreaOutputType.Polygons
        self.service_area.geometryAtOverlap = arcpy.nax.ServiceAreaOverlapGeometry.Split
    
    """
    Computes a polygon representing the service area surrounding a central point represented 
    by the facilities layer.

    Args:
        facilities_layer (str): string location of feature layer containing the central point from 
             which the service area is calculated
        compare_layer (str): string location of feature layer containing points to check for 
            intersection with the service area polygon 
    
    Return:
        string location of feature layer containing the points of compare_layer located within the 
            service area polygon
    """
    def compute_intersection(self, facilities_layer, compare_layer):
        # Load The intersection
        self.service_area.load(arcpy.nax.ServiceAreaInputDataType.Facilities, facilities_layer)

        # Solve the service area
        polygon_result = self.service_area.solve()

        # Export the result to a feature class if the solve was successful
        sa_polygon_layer = r"memory\tmp_sa_polygon"
        if polygon_result.solveSucceeded:
            polygon_result.export(arcpy.nax.ServiceAreaOutputDataType.Polygons, sa_polygon_layer)
        else:
            raise RuntimeError("Service Area solve failed")
        
        # Compute the actual intersection
        intesection_results = arcpy.management.SelectLayerByLocation(
            in_layer=compare_layer,
            overlap_type="INTERSECT",
            select_features=sa_polygon_layer,
            search_distance=None,
            selection_type="NEW_SELECTION",
            invert_spatial_relationship="NOT_INVERT"
        )
        # Error checking?
        # if intersections_results.status != 4:
        #     raise RuntimeError("Intersection calculation failed")

        # Copy the intersection result to a new feature layer in memory with a random name
        intersection_layer = r"memory\interseciton_" + uuid.uuid4().hex
        arcpy.management.CopyFeatures(intesection_results, intersection_layer)

        return intersection_layer
