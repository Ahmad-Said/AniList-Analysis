# Here we define our query as a multi-line string
import math
from io import BytesIO

import numpy as np
import pandas as pandas
import requests as requests
from IPython.core.display_functions import display
from PIL import Image as pil_image

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
variables = {"page": 1, "perPage": 25}
url = 'https://graphql.anilist.co'

response = requests.post(url, json={'query': query, 'variables': variables})

resultDict = response.json()['data']['Page']['characters']
resultDataFrame = pandas.json_normalize(resultDict)

all_images = []

for character in resultDict:
    print("Extracting picture of ", character['name']['full'], " from ", character['image']['medium'])
    img_response = requests.get(character['image']['medium'])
    all_images.append(pil_image.open(BytesIO(img_response.content)))

min_shape = sorted([(np.sum(i.size), i.size) for i in all_images])[0][1]
all_images = [img.resize(min_shape) for img in all_images]

widths, heights = zip(*(i.size for i in all_images))

# number of image per row
m = col_size = 5
n = row_size = math.ceil(len(all_images) / m)
#

final = [all_images[i * m:(i + 1) * m] for i in range((len(all_images) + m - 1) // m )]

total_width = max(widths) * m
total_height = max(heights) * n
#
new_im = pil_image.new('RGB', (total_width, total_height))
#
y_offset = 0
for horizontal_imgs in final:
    x_offset = 0
    for im in horizontal_imgs:
        new_im.paste(im, (x_offset, y_offset))
        x_offset += im.size[0]
    y_offset += im.size[1]
#
new_im.show();
display(new_im)
# new_im.save('test.jpg')