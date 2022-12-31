# Here we define our query as a multi-line string
import requests as requests
import pandas as pandas
import json as json

url = 'https://graphql.anilist.co'

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

# Extracting first page
variables = {
    'year': 2020,
    'page': 1,
    'perPage': 5
}


def get_data_from_page(page):
    variables['page'] = page
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()['data']['Page']['media']


data = []
for i in range(1,4):
    print("Extracting page ", i)
    data += get_data_from_page(1)

# forming dataframe from collected data
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
resultDataFrame = pandas.DataFrame(data)
resultDataFrame

