import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor

postgresConn = psycopg2.connect(database="admin",
                                host="localhost",
                                user="admin",
                                password="admin",
                                port="5433")

# cursor = postgresConn.cursor()
# cursor.execute("select o.name as name, armes.attackpower from armes join objet o on o.object_id = armes.object_id")
# row = cursor.fetchone()

cursor = postgresConn.cursor(cursor_factory=RealDictCursor)

cursor.execute("select joueur_id, username, password, sex from joueur join sex s on s.sex_id = joueur.sex_id")

for c in cursor.fetchall():
    c['price'] =  c["joueur_id"] * 0.5 * 0.1
    print(c['username'], " have for current year ", 2020, c['price'])

