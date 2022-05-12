from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import json

# Overpass query builder solution
by = Nominatim().query('Belarus')
# Selsavets and raion-level importance cities
query8 = overpassQueryBuilder(area=by.areaId(), elementType=[
    'relation'], selector='"admin_level"="8"', includeGeometry=True)
selsavet = Overpass().query(query8)
# Voblasts-level importance cities
query6 = overpassQueryBuilder(area=by.areaId(), elementType=[
    'relation'], selector=['"admin_level"="6"', '"place"="city"'], includeGeometry=True)
vobl = Overpass().query(query6)
# Voblasts-level importance towns (Zhodzina only)
query6t = overpassQueryBuilder(area=by.areaId(), elementType=[
    'relation'], selector=['"admin_level"="6"', '"place"="town"'], includeGeometry=True)
voblt = Overpass().query(query6t)
# Kupa (Narach) is not included
narach = Overpass().query("relation(6722721);out body geom;")
# Region-level importance cities (Minsk only)
query4 = overpassQueryBuilder(area=by.areaId(), elementType=[
    'relation'], selector=['"admin_level"="4"', '"place"="city"'], includeGeometry=True)
minsk = Overpass().query(query4)

final_json = {"type": "FeatureCollection", "features": []}
sss = selsavet.elements()
for ss, i in zip(sss, range(len(sss))):
    poly = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": ss.geometry()}
    final_json["features"].append(poly)
cs = vobl.elements()
for c, i in zip(cs, range(len(sss), len(sss)+len(cs))):
    poly = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": c.geometry()}
    final_json["features"].append(poly)
zs = voblt.elements()
for z, i in zip(zs, range(len(sss)+len(cs), len(sss)+len(cs)+len(zs))):
    poly = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": z.geometry()}
    final_json["features"].append(poly)
n = narach.elements()[0]
poly = {"type": "Feature",
        "properties": {"name": str(len(sss)+len(cs)+len(zs))},
        "geometry": n.geometry()}
final_json["features"].append(poly)
m = minsk.elements()[0]
poly = {"type": "Feature",
        "properties": {"name": str(len(sss)+len(cs)+len(zs)+1)},
        "geometry": m.geometry()}
final_json["features"].append(poly)

with open("final_json.geojson", "w") as f:
    json.dump(final_json, f)
