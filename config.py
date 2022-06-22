import certifi
import pymongo

con_str = "mongodb+srv://aldrian1:test123@cluster0.ijmyb.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("CrazyStore")
