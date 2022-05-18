from shapely.geometry import MultiPolygon, Polygon, mapping
from shapely.ops import unary_union
import argparse
import json

parser = argparse.ArgumentParser(
    description='Utility that composes regions from selsavets')

parser.add_argument('--infile', help='File with selsavets')
parser.add_argument('--scheme', help='File with the merge scheme')
parser.add_argument('--outfile', help='Output file')

args = parser.parse_args()

# The first member in every line is the name
names = []
with open(args.scheme) as f:
    lines = f.read().split('\n')[:-1]
    names = [l.split(',')[0] for l in lines]
    colors = [l.split(',')[1] for l in lines]
    pavets = [[int(s.strip()) for s in l.split(',')[2:]] for l in lines]

infile = open(args.infile)
selsavets = json.load(infile)['features']
infile.close()

pavet_polygons = []
for pavet in pavets:
    ppolys = []
    for ss in pavet:
        plist = selsavets[ss]['geometry']
        if plist['type'] == 'Polygon':
            poly = Polygon(plist['coordinates'][0])
            ppolys.append(poly)
        elif plist['type'] == 'MultiPolygon':
            mpoly = MultiPolygon([Polygon(poly[0])
                                 for poly in plist['coordinates']])
            ppolys.append(mpoly)

    pavet_polygons.append(unary_union(ppolys))

with open(args.outfile, "w") as outfile:
    final_output = {"type": "FeautureCollection", "features": []}
    for pavet_polygon, name, color in zip(pavet_polygons, names, colors):
        feature = {'type': "Feature", "properties": {"name": name, "_umap_options": {"color": color}},
                   "geometry": mapping(pavet_polygon)}
        final_output["features"].append(feature)
    json.dump(final_output, outfile)

print(args)
