from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

def cleanup_old_collections() -> None:
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    db = client["Velib"]
    
    # Define the time threshold (2 weeks)
    two_weeks_ago = datetime.now(timezone.utc) - timedelta(minutes==2)
    
    for collection_name in db.list_collection_names():
        try:
            # Extract timestamp from collection name
            timestamp = int(collection_name.split('_')[-1])
            collection_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)  # Ensure collection time is UTC aware
            if collection_time < two_weeks_ago:
                # Drop the collection if it's older than 2 weeks
                db.drop_collection(collection_name)
                print(f"Dropped collection: {collection_name}")
        except Exception as e:
            print(f"Error cleaning up collection {collection_name}: {e}")

if __name__ == "__main__":
    cleanup_old_collections()
