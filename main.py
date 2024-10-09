import calendar
from codecs import Codec
import time
from typing import Any, Dict, List, Optional
from pymongo.collection import Collection
from pymongo import MongoClient
import requests
from requests.exceptions import HTTPError

def get_data(offset: int) -> Optional[List[Dict[str, Any]]]:
    try:
        r = requests.get(f"https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100&offset={offset}")
        r.raise_for_status()
        jsonResponse = r.json()
        return jsonResponse.get("results")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def conn() -> tuple[Collection, str]:
    CONNECTION_STRING = "mongodb://localhost:27017"  
    client = MongoClient(CONNECTION_STRING)
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    db = client["Velib"]
    collection_name = f"velo_libre_{ts}"
    collection = db[collection_name]
    return collection, collection_name

def set_data(client: Collection, data: List[Dict[str, Any]]) -> None:
    try:
        client.insert_many(data)
    except Exception as err:
        print(f"Error: {err}")

def get_total_count() -> Optional[int]:
    try:
        r = requests.get(f"https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=1&offset=0")
        r.raise_for_status()
        jsonResponse = r.json()
        return jsonResponse.get("total_count")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def  init() -> None:
    collection, collection_name = conn()
    total_count = get_total_count()
    if total_count is not None:
        for offset in range(0, total_count, 100):
            data = get_data(offset)
            if data:
                set_data(collection, data)

    #map_function = Codec("""
    #function() {
    #    emit(this.nom_arrondissement_communes, 1);
    #}
    #""")

    #reduce_function = Codec("""
    #function(key, values) {
    #    return Array.sum(values);
    #}
    #""")

    #result = collection.database.command(
     #   'mapReduce',
      #  collection_name,
       # map=map_function,
        #reduce=reduce_function,
        #out={'inline': 1}
    #)

    # Sort the results
    #sorted_results = sorted(result['results'], key=lambda x: x['value'], reverse=True)

    # Print the results
    #for doc in sorted_results:
     #   print(f"Arroundissement: {doc['_id']}, Nombre de vélib disponible: {doc['value']}")

if __name__ == "__main__":
    init()