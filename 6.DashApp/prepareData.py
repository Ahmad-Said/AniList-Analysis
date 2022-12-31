from pandas.io.json import json_normalize

from importData import *

#  prepare data
mediaTitles = json_normalize(datasetMedias['title'].tolist()).add_prefix('title_')
# convert types of columns to string
if len(datasetMedias.filter(like="title_").columns) == 0:
    datasetMedias = mediaTitles.join(datasetMedias)
else:
    print("Already flattened media titles")


def flattenStaffNames():
    global datasetStaffs
    # flatten staff names
    staffNames = json_normalize(datasetStaffs['name'].tolist()).add_prefix('name_')
    # convert types of columns to string
    if len(datasetStaffs.filter(like="name_").columns) == 0:
        datasetStaffs = staffNames.join(datasetStaffs)
    else:
        print("Already flattened staff names")


flattenStaffNames()
datasetMedias.index = datasetMedias.id
datasetStaffs.index = datasetStaffs.id
mediaTitles.index = datasetMedias.index

print("preparation complete")
