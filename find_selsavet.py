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
# Arexausk is not included
arexausk = Overpass().query("relation(6809905);out body geom;")

final_json = {"type": "FeatureCollection", "features": []}
node_json = {"type": "FeatureCollection", "features": []}
pcenters_json = {"type": "FeatureCollection", "features": []}

sss = selsavet.elements()
for ss, i in zip(sss, range(len(sss))):
    poly = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": ss.geometry()}
    final_json["features"].append(poly)
    node = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": None}
    for memb in ss.members():
        if memb.type() == 'node':
            node["geometry"] = memb.geometry()
            break
    node_json["features"].append(node)
    if "place" in ss.tags():
        pcenters_json["features"].append(node)
cs = vobl.elements()
for c, i in zip(cs, range(len(sss), len(sss)+len(cs))):
    poly = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": c.geometry()}
    final_json["features"].append(poly)
    node = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": None}
    for memb in c.members():
        if memb.type() == 'node':
            node["geometry"] = memb.geometry()
            break
    node_json["features"].append(node)
    if "place" in c.tags():
        pcenters_json["features"].append(node)
zs = voblt.elements()
for z, i in zip(zs, range(len(sss)+len(cs), len(sss)+len(cs)+len(zs))):
    poly = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": z.geometry()}
    final_json["features"].append(poly)
    node = {"type": "Feature",
            "properties": {"name": str(i)},
            "geometry": None}
    for memb in z.members():
        if memb.type() == 'node':
            node["geometry"] = memb.geometry()
            break
    node_json["features"].append(node)
    if "place" in z.tags():
        pcenters_json["features"].append(node)
n = narach.elements()[0]
poly = {"type": "Feature",
        "properties": {"name": str(len(sss)+len(cs)+len(zs))},
        "geometry": n.geometry()}
final_json["features"].append(poly)
node = {"type": "Feature",
        "properties": {"name": str(i)},
        "geometry": None}
for memb in n.members():
    if memb.type() == 'node':
        node["geometry"] = memb.geometry()
        break
    node_json["features"].append(node)
m = minsk.elements()[0]
poly = {"type": "Feature",
        "properties": {"name": str(len(sss)+len(cs)+len(zs)+1)},
        "geometry": m.geometry()}
final_json["features"].append(poly)
node = {"type": "Feature",
        "properties": {"name": str(i)},
        "geometry": None}
for memb in m.members():
    if memb.type() == 'node':
        node["geometry"] = memb.geometry()
        break
    node_json["features"].append(node)
    if "place" in m.tags():
        pcenters_json["features"].append(node)
a = arexausk.elements()[0]
poly = {"type": "Feature",
        "properties": {"name": str(len(sss)+len(cs)+len(zs)+2)},
        "geometry": a.geometry()}
final_json["features"].append(poly)
node = {"type": "Feature",
        "properties": {"name": str(i)},
        "geometry": None}
for memb in a.members():
    if memb.type() == 'node':
        node["geometry"] = memb.geometry()
        break
    node_json["features"].append(node)

with open("boundaries.geojson", "w") as f:
    json.dump(final_json, f)
with open("centers.geojson", "w") as f:
    json.dump(node_json, f)
with open("pcenters.geojson", "w") as f:
    json.dump(pcenters_json, f)
