import pandas
from numpy import character
from pymongo import MongoClient

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://admin:admin@localhost:27017/?authMechanism=DEFAULT')

# insert into database
characters = pandas.read_json("medias.json").rename(columns={"id": "_id"})

# insert each 100 entries together
insert_batch_nb = 100
i = 0
data = []
for index, character in characters.iterrows():
    data.append(dict(character))
    i += 1
    if i == insert_batch_nb:
        i = 0
        try:
            databaseResponse = client['myDatabaseTest']['Media'].insert_many(data, ordered=False)
        except Exception as e:
            print(e)

databaseResponse = client['myDatabaseTest']['Media'].insert_many(data, ordered=False)

# select from database
# filter={
#     'age': 26
# }
#
# result = client['myDatabaseTest']['CharactersTranspose'].find(
#     filter=filter
# )
#
# print(result.next())
