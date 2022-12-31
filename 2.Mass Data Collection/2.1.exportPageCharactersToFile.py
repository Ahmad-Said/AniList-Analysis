# Here we define our query as a multi-line string
import requests as requests
import pandas as pandas
import json as json

from IPython.core.display_functions import display

url = 'https://graphql.anilist.co'

query = '''
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    characters {
      name {
        first
        middle
        last
        full
        native
        userPreferred
      }
      gender
      age
      dateOfBirth {
        month
        day
      }
      description
      siteUrl
      favourites
      image {
        medium
      }
      media {
        edges {
          node {
            id
          }
        }
      }
    }
  }
}
'''

# Extracting first page
variables = {
    "page": 1,
    "perPage": 50
}

data = []
has_next_page = True
page_NB = 1
while has_next_page:
    print(f"records {len(data)} Extracting page {page_NB}")
    variables['page'] = page_NB
    response = requests.post(url, json={'query': query, 'variables': variables})
    data += response.json()['data']['Page']['characters']
    page_NB += 1
    has_next_page = False

# forming dataframe from collected data
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
resultDataFrame = pandas.DataFrame(data).transpose()
resultDataFrame.to_json("characters_1Page.json")
display(resultDataFrame)

testing = pandas.read_json("characters_1Page.json")

