import arcpy

class HousingData:
    def __init__(self, public_active=True, affordable_active=True):
        # Load Public and Affordable points into memory
        self.public_layer = str(arcpy.conversion.FeatureClassToFeatureClass(
            r"C:\Users\gre13341\Documents\Hackathon\data\hackathon_housing.gdb\PublicHousing_Points", 
            "memory",
            "PublicHousing" 
        ))
        self.affordable_layer = str(arcpy.conversion.FeatureClassToFeatureClass(
            r"C:\Users\gre13341\Documents\Hackathon\data\hackathon_housing.gdb\Affordable_Housing", 
            "memory",
            "AffordableHousing" 
        ))

        self.public_active = public_active
        self.affordable_active = affordable_active
    
    # def filter_by_neighborhood(self, neighborhood):
    #     neighborhood_layer = str(arcpy.management.SelectLayerByAttribute(
    #         in_layer_or_view=r"C:\Users\gre13341\Documents\Hackathon\data\hackathon_neighborhoods.gdb\Neighborhood_Clusters",
    #         selection_type="NEW_SELECTION",
    #         where_clause=f"NBH_NAMES contains '%{neighborhood}%'",
    #         invert_where_clause=None
    #     ))

    #     if self.public_active:
    #         intesection_results = arcpy.management.SelectLayerByLocation(
    #             in_layer=self.public_layer, 
    #             overlap_type="INTERSECT",
    #             select_features=,
    #             search_distance=None,
    #             selection_type="NEW_SELECTION",
    #             invert_spatial_relationship="NOT_INVERT"
    #         )
    
    def filter_by_cluster(self, cluster):
        # Get the polygon named `cluster`
        cluster_layer = str(arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=r"C:\Users\gre13341\Documents\Hackathon\data\hackathon_neighborhoods.gdb\Neighborhood_Clusters",
            selection_type="NEW_SELECTION",
            where_clause=f"NAME='{cluster}'",
            invert_where_clause=None
        ))

        public_cluster_layer = None
        if self.public_active:
            # Find public locations in the neighborhood
            public_cluster_results = arcpy.management.SelectLayerByLocation(
                in_layer=self.public_layer, 
                overlap_type="INTERSECT",
                select_features=cluster_layer,
                search_distance=None,
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"
            )

            public_cluster_layer = fr"memory\{cluster}"
            arcpy.management.CopyFeatures(public_cluster_results, public_cluster_layer)          

        affordable_cluster_layer = None
        if self.affordable_active:
            # Find affordable locations in the neighborhood
            affordable_cluster_results = arcpy.management.SelectLayerByLocation(
                in_layer=self.affordable_layer, 
                overlap_type="INTERSECT",
                select_features=cluster_layer,
                search_distance=None,
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"
            )

            affordable_cluster_layer = fr"memory\{cluster}"
            arcpy.management.CopyFeatures(affordable_cluster_results, affordable_cluster_layer)  
        
        return public_cluster_layer, affordable_cluster_layer
