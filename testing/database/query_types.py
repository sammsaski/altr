import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.Client.from_service_account_json(os.getcwd() + '/firestore-key.json')

data = db.collection('properties').document('4ZJAXxJIyrx8kmIcW8wr').get().to_dict()

print(data)