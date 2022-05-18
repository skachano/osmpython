from shapely.geometry import MultiPolygon, Polygon, mapping
from shapely.ops import unary_union
import argparse
import json

parser = argparse.ArgumentParser(
    description='Utility that composes regions from selsavets')

parser.add_argument('--infile', help='File with borders')
parser.add_argument('--pavet', help='Pavet with borders to adjust')
parser.add_argument('--ref', help='Pavet with reference borders')
parser.add_argument('--outfile', help='Output file')

args = parser.parse_args()

infile = open(args.infile)
pavets = json.load(infile)['features']
infile.close()

name_dict = {p["properties"]["name"]: p for p in pavets}

geo_pavet = name_dict[args.pavet]["geometry"]
if geo_pavet['type'] == 'Polygon':
    poly_pavet = Polygon(geo_pavet["coordinates"][0])
elif geo_pavet['type'] == 'MultiPolygon':
    poly_pavet = MultiPolygon([Polygon(poly[0])
                               for poly in geo_pavet["coordinates"]])
geo_ref = name_dict[args.ref]["geometry"]
if geo_ref['type'] == 'Polygon':
    poly_ref = Polygon(geo_ref["coordinates"][0])
elif geo_ref['type'] == 'MultiPolygon':
    poly_ref = MultiPolygon([Polygon(poly[0])
                             for poly in geo_ref["coordinates"]])

poly_pavet = poly_pavet.difference(poly_ref)

name_dict[args.pavet]["geometry"] = mapping(poly_pavet)
features = [f for n, f in name_dict.items()]
final_output = {"type": "FeautureCollection", "features": features}

with open(args.outfile, "w") as outfile:
    json.dump(final_output, outfile)
