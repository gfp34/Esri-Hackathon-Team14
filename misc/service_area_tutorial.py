"""Find an area that is within 2.5 kilometers (1.55 miles) of walking distance from an elementry school."""

import arcgis
import pandas as pd


def print_result(result):
    """Print useful information from the result."""
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)

    output_polygons = arcgis.features.FeatureSet.from_dict(result["saPolygons"]).sdf
    print("\n-- Output Polygons -- \n")
    print(output_polygons[["Name", "FromBreak", "ToBreak"]].to_string(index=False))


def main():
    """Program execution logic."""

    # inputs
    facilities = "-117.133163,34.022445"

    # Connect to the Service area service and call it
    api_key = "AAPKcbf8118c14454e038f0f8f49acd67ecbK881HtN8H-5A3V1Rydhsy781gAIvcTSuytUP7ctrJS76H_MIqra_ii2zLyhUfngq"
    portal = arcgis.GIS("https://www.arcgis.com", api_key=api_key)
    service_area = arcgis.network.ServiceAreaLayer(portal.properties.helperServices.serviceArea.url,
                                                   gis=portal)
    # Get the walking distance travel mode defined for the portal. Fail if the travel mode is not found.
    walking_distance_travel_mode = ""
    for feature in arcgis.network.analysis.get_travel_modes().supported_travel_modes.features:
        attributes = feature.attributes
        if attributes["AltName"] == "Walking Distance":
            walking_distance_travel_mode = attributes["TravelMode"]
            break
    assert walking_distance_travel_mode, "Walking Distance travel mode not found"

    result = service_area.solve_service_area(facilities=facilities,
                                             default_breaks=[2.5],
                                             travel_direction="esriNATravelDirectionToFacility",
                                             travel_mode=walking_distance_travel_mode)
    print_result(result)



if __name__ == "__main__":
    main()