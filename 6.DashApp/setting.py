# settings.py
import pandas as pd

jsonMediaPath = '../data/medias.json'
jsonMediaPartialPath = '../data/split/medias/medias1.json'
jsonStaffPath = '../data/staffs.json'
jsonStaffPartialPath = '../data/split/staffs/staffs1.json'
# usePartialJsonPath = [True, True]
usePartialJsonPath = [False, False]

readJsonColMedias = ['id', 'title', 'siteUrl', 'relations', 'staff']
readJsonColStaff = ['id', 'name', 'siteUrl']

# columns to display in bootstrap table
# only title and name are exploded at runtime with prefix title_field and name_field
# All columns must be included in read json in able to display them
displayMediaColumns = ['id', 'title_userPreferred', 'siteUrl']
displayStaffColumns = ['id', 'name_userPreferred', 'siteUrl']

# disable warning on changing copy of slice of dataframe
pd.options.mode.chained_assignment = None  # default='warn'

# prevent consecutive update of filter output in interval of x second (recommended 0.5 second depend on your machine)
# preventConsecutiveUpdate = [False]
preventConsecutiveUpdate = [True, 0.5]

# display graph with media as parent node
showMediaNodeByDefault = [False]
# ignore media in the list where it doesn't have any connection between staffs
removeMediaOutlierByDefault = [False]

# ignore media in the list where it doesn't have any connection between staffs
staffAtLeastInXMedia = [1]
nodeGraphEspacement = [30]


stylesheetGraph=[
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },

    # Class selectors
    {
        'selector': '.red',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {
        'selector': '.triangle',
        'style': {
            'shape': 'triangle'
        }
    }
]


# Runtime variable do not change
# global variable to collect filtered medias
# usage targetMediasGl[0] = Dataframe...
# medias = targetMediasGl[0]
targetMediasGl = ['']
