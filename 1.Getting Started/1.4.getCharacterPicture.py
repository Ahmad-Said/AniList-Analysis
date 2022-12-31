# Here we define our query as a multi-line string
import requests as requests
import pandas as pandas
import os as os
from PIL import Image as img
from io import BytesIO
from IPython.display import Image, display

query = '''
query ($page: Int, $perPage: Int) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
        characters(sort: FAVOURITES_DESC, isBirthday : true){
            name {
              full
            }
            dateOfBirth {
              month
              day
            }
            favourites  
            image {
              medium
            }
      }
    }
}
'''
variables = {
    'page': 1,
    'perPage': 10
}
url = 'https://graphql.anilist.co'

response = requests.post(url, json={'query': query, 'variables': variables})

resultDict = response.json()['data']['Page']['characters']
resultDataFrame  = pandas.json_normalize(resultDict)
resultDataFrame

name_to_image = dict()

for character in resultDict:
    print("Extracting picture of ", character['name']['full'], " from ", character['image']['medium'])
    img_response = requests.get(character['image']['medium'])
    img_data = img_response.content
    img_path = img_response.headers['x-bz-file-name']
    name_to_image[character['name']['full']] = img.open(BytesIO(img_response.content))
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    with open(img_response.headers['x-bz-file-name'], 'wb') as handler:
        handler.write(img_data)

for name in list(name_to_image.keys())[5:]:
    print(name)
    display(name_to_image[name])
