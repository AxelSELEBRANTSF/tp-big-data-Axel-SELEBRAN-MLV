import json
from pymongo import MongoClient
import webbrowser
import folium

# Given point (center of the map)
CENTRAL_POINT = [48.90808780293388, 2.3665120103670043]

def get_database_and_collection():
    """Connect to MongoDB and get the most recent collection."""
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    db = client["Velib"]
    
    collection_names = db.list_collection_names()
    velo_libre_collections = [name for name in collection_names if name.startswith("velo_libre_")]
    
    if not velo_libre_collections:
        raise ValueError("No matching collections found")
    
    most_recent_collection_name = max(velo_libre_collections)
    return db, most_recent_collection_name

def get_ordered_list(points, x, y):
    """Sort points based on distance to a given coordinate (x, y)."""
    return sorted(points, key=lambda p: (p['lat'] - x)**2 + (p['lon'] - y)**2)

def format_points(collection):
    """Format the points to include lat, lon, and name."""
    formatted_list = []
    for point in collection.find({}, {"coordonnees_geo": 1, "name": 1}):
        try:
            coordinates = point['coordonnees_geo']
            if isinstance(coordinates, str):
                coordinates = json.loads(coordinates)
            
            formatted_list.append({
                'lat': float(coordinates['lat']),
                'lon': float(coordinates['lon']),
                'name': point.get('name', 'Unknown')
            })
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error parsing point: {point}, error: {e}")
    return formatted_list

def create_map(points, center):
    """Create a Folium map with markers for the given points."""
    map = folium.Map(location=center, zoom_start=15)
    
    # Add the points to the map
    for p in points:
        folium.Marker([p['lat'], p['lon']], popup=p['name']).add_to(map)
    
    # Mark the central point on the map
    folium.Marker(center, popup="Vous êtes ici.", icon=folium.Icon(color='red', icon='info-sign')).add_to(map)
    
    return map

def main():
    try:
        # Connect to the database and get the most recent collection
        db, collection_name = get_database_and_collection()
        collection = db[collection_name]
        
        # Format the points
        formatted_points = format_points(collection)
        
        # Get the 15 closest points to the central point
        closest_points = get_ordered_list(formatted_points, CENTRAL_POINT[0], CENTRAL_POINT[1])[:15]
        
        # Create the map
        map = create_map(closest_points, CENTRAL_POINT)
        
        # Save and open the map
        map.save("velib_map.html")
        webbrowser.open("velib_map.html")
        
        print(f"Map created successfully using collection: {collection_name}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()