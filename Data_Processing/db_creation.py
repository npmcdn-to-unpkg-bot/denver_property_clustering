from pymongo import MongoClient

client = MongoClient()
db = client.denver_properties

json_file = 'liquor_lic.json'

db.liq_lic.insert_many(json_file)
