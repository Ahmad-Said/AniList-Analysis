import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient

mongoClient = MongoClient('mongodb://admin:admin@localhost:27017/?authMechanism=DEFAULT')

postgresConn = psycopg2.connect(database="admin",
                                host="localhost",
                                user="admin",
                                password="admin",
                                port="5433")

# cursor = postgresConn.cursor()
# cursor.execute("select o.name as name, armes.attackpower from armes join objet o on o.object_id = armes.object_id")
# row = cursor.fetchone()

ps_cursor = postgresConn.cursor(cursor_factory=RealDictCursor)

ps_cursor.execute("select * from joueur")

result = mongoClient.get_database("FAQ").get_collection("Joueur").insert_many([dict(rowconv) for rowconv in ps_cursor.fetchall()])

print(result)
