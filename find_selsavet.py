from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import json

# Overpass query builder solution
by = Nominatim().query('Belarus')
query = overpassQueryBuilder(area=by.areaId(), elementType=[
    'relation'], selector='"admin_level"="8"', includeGeometry=True)
results = Overpass().query(query)

final_json = {"type": "FeatureCollection", "features": []}
for ss in results.elements():
    poly = {"type": "Feature",
            "name": ss.tag("intl_name"),
            "geometry": ss.geometry()}
    final_json["features"].append(poly)

with open("final_json.geojson", "w") as f:
    json.dump(final_json, f)
