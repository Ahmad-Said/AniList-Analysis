# Here we define our query as a multi-line string
import requests as requests
import pandas as pandas
import json as json

query = '''
query ($id: Int, $page: Int, $perPage: Int, $year : Int) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        media (id: $id, season: WINTER, seasonYear: $year) {
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
}
'''
variables = {
    'year': 2020,
    'page': 1,
    'perPage': 10
}
url = 'https://graphql.anilist.co'

response = requests.post(url, json={'query': query, 'variables': variables})

resultDict = response.json()['data']['Page']['media']
resultDataFrame  = pandas.json_normalize(resultDict)
resultDataFrame
