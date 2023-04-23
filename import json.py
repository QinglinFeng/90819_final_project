import json

# Replace this with the path to your GeoJSON file
geojson_file = "pittsburgh_neighborhoods.geojson"

with open(geojson_file, "r") as file:
    geojson_data = json.load(file)

for feature in geojson_data["features"]:
    neighborhood_name = feature["properties"]["hood"]
    print(neighborhood_name)
