# Here we define our query as a multi-line string
import requests as requests
import pandas as pandas
import json as json

query = '''
query ($title: String) 
{
  media (search : $title) {
    id
    title {
      romaji
      english
      native
      userPreferred
    }
    season
    seasonYear
    source
    episodes
    popularity
  }
}
'''

# Define our query variables and values that will be used in the query request
variables = {
    'title': 'Cowboy Bebop'
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request
response = requests.post(url, json={'query': query, 'variables': variables})
resultDict = response.json()['data']['media']
resultDataFrame  = pandas.json_normalize(resultDict)


