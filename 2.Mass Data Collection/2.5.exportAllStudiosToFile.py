# Here we define our query as a multi-line string
import requests as requests
import pandas as pandas
import time as time

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
    studios {
      id
      name
      isAnimationStudio
      media {
        edges {
          isnode {
            id
          }
        }
      }
      siteUrl
      isFavourite
      favourites
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
number_of_request_per_batch = 80
wait_time_between_batch_in_seconds = 100

print("Stop at any time with Ctrl+C")
print(f"Collecting studios informations {number_of_request_per_batch} requests per {wait_time_between_batch_in_seconds}+ seconds")
try:
    while has_next_page:
        total_requests = 0
        while has_next_page and total_requests < number_of_request_per_batch:
            print(f"records {len(data)} Extracting page {page_NB}")
            variables['page'] = page_NB
            response = requests.post(url, json={'query': query, 'variables': variables})
            has_next_page = response.json()['data']['Page']['pageInfo']['hasNextPage']
            data += response.json()['data']['Page']['studios']
            page_NB += 1
            total_requests += 1
        print(f"Waiting {wait_time_between_batch_in_seconds} seconds...")
        time.sleep(wait_time_between_batch_in_seconds)
except KeyboardInterrupt:
    print("interrupted by user")
except Exception as e:
    print("An exception occurred")
    print(e)


# forming dataframe from collected data
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
resultDataFrame = pandas.DataFrame(data)
resultDataFrame.to_json("studios.json")
display(resultDataFrame)
