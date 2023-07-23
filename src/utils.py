import arcpy
import tempfile

def layer_to_json_str(feature_layer):
    tmpf = tempfile.NamedTemporaryFile(suffix="_feature_layer.json")
    arcpy.conversion.FeaturesToJSON(feature_layer, tmpf.name)
    json_str = tmpf.read()
    tmpf.close()
    return json_str

