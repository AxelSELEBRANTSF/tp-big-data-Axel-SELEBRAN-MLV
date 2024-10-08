import json
from pymongo import MongoClient
import webbrowser
import folium

coor_entre = [48.90808780293388, 2.3665120103670043]  # Given point

# Function to sort the points based on distance to a given coordinate (x, y)
def get_ordered_list(points, x, y):
    points.sort(key=lambda p: (p['lat'] - x)**2 + (p['lon'] - y)**2)
    return points

# Function to connect to MongoDB
def get_database():
    CONNECTION_STRING = "mongodb://localhost:27018"  
    client = MongoClient(CONNECTION_STRING)
    return client["Velib"]

# Get the database
dbName = get_database()
listNameDB = dbName.list_collection_names()
strNameDB = listNameDB[-1]

# Query to get all points including coordinates and name fields

get_list_points = dbName[strNameDB]
list_points = get_list_points.find({}, {"coordonnees_geo": 1, "name": 1})

# Format the points to include lat, lon, and name
# Convert 'coordonnees_geo' from JSON string and ensure 'lat' and 'lon' are floats
formatted_list = []

for point in list_points:
    try:
        # Convert the 'coordonnees_geo' string (dictionary format) to a Python object (dict)
        coordinates = json.loads(point['coordonnees_geo'])
        
        # Ensure we extract 'lat' and 'lon' from the dictionary
        formatted_list.append({
            'lat': float(coordinates['lat']), 
            'lon': float(coordinates['lon']), 
            'name': point.get('name', 'Unknown')
        })
    except (ValueError, KeyError) as e:
        print(f"Error parsing point: {point}, error: {e}")

# Get the 15 closest points to the given coordinate (coor_entre)
ordered_points = get_ordered_list(formatted_list, coor_entre[0], coor_entre[1])
closest_fifteen_points = ordered_points[:15]

# Create a Folium map centered on the given point
map = folium.Map(location=coor_entre, zoom_start=15)

# Add the 15 closest points to the map with their names as popups
for p in closest_fifteen_points:
    folium.Marker([p['lat'], p['lon']], popup=p['name']).add_to(map)

# Mark the given point on the map
folium.Marker(coor_entre, popup="Vous êtes ici.").add_to(map)

# Save and open the map
map.save("map.html")
webbrowser.open("map.html")
