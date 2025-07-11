from bson import ObjectId
from flask import current_app

def get_all_places():
    return list(current_app.mongo.db.batik_places.find())

def get_place_by_id(place_id):
    return current_app.mongo.db.batik_places.find_one({"_id": ObjectId(place_id)})

def create_place(data):
    return current_app.mongo.db.batik_places.insert_one(data)

def update_place(place_id, update_data):
    return current_app.mongo.db.batik_places.update_one(
        {"_id": ObjectId(place_id)},
        {"$set": update_data}
    )

def delete_place(place_id):
    return current_app.mongo.db.batik_places.delete_one({"_id": ObjectId(place_id)})

def get_all_places_api():
    return list(current_app.mongo.db.batik_places.find({}, {"_id": 0}))
