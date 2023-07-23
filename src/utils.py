import arcpy
import os
import tempfile
import uuid

def layer_to_json_str(feature_layer):
    tmp_name = uuid.uuid4().hex + '_feature_layer.json'
    tmp_path = os.path.join(tempfile.gettempdir(), tmp_name)
    arcpy.conversion.FeaturesToJSON(feature_layer, tmp_path)
    with open(tmp_path, 'r') as tmpf:
        json_str = tmpf.read()
    os.remove(tmp_path)
    return json_str

