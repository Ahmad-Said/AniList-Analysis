from datetime import datetime
from pymongo import MongoClient
import bson


bson.objectid.ObjectId
client = MongoClient('mongodb://admin:admin@localhost:27017/?authMechanism=DEFAULT')


myQuestion = {
    'title': 'comment beat boos lvl 1',
    'description': {
        "joueur_id" : 1,
        "text": "this is the dfawjef pjaweif pjawieopf jwaei pfjawe",
        "date": datetime.today().now(),
        "nom_joueur": "dark"
    },
    'reponses':[{
        "_id" : bson.objectid.ObjectId(),
        "joueur_id" : 2,
        "text": "this aefaew fpjawieopf jwaei pfjawe",
        "date": datetime.today().now(),
        "nom_joueur": "dark"
    },
        {
            "_id" : bson.objectid.ObjectId(),
            "joueur_id" : 3,
            "text": "this awefawef pfjawe",
            "date": datetime.today().now(),
            "nom_joueur": "dark"
        }

    ]
}

client.get_database("FAQ").get_collection("Sujet").insert_one(myQuestion)