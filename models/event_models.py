from bson import ObjectId
from config import event_col

def get_all_events():
    return list(event_col.find())

def get_event_by_id(event_id):
    return event_col.find_one({"_id": ObjectId(event_id)})

def create_event(data):
    return event_col.insert_one(data)

def update_event(event_id, update_data):
    return event_col.update_one({"_id": ObjectId(event_id)}, {"$set": update_data})

def delete_event(event_id):
    return event_col.delete_one({"_id": ObjectId(event_id)})
