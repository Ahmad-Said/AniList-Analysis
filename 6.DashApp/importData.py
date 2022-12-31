# reading data
import gc
import warnings

import pandas

import setting

# https://plotly.com/python/network-graphs/
# read dataset from json file
# https://github.com/catboost/catboost/issues/2179
warnings.simplefilter(action='ignore', category=FutureWarning)
print("clearing memory")
datasetMedias = None
datasetStaffs = None
gc.collect()
print("reading medias")
datasetMedias = pandas.read_json(setting.jsonMediaPartialPath if setting.usePartialJsonPath[0] else setting.jsonMediaPath)
datasetMedias = datasetMedias[setting.readJsonColMedias]
print("reading medias complete " + str(len(datasetMedias)) + " entries")
print("reading staffs")
datasetStaffs = pandas.read_json(setting.jsonStaffPartialPath if setting.usePartialJsonPath[1] else setting.jsonStaffPath)
datasetStaffs = datasetStaffs[setting.readJsonColStaff]
print("reading staffs complete " + str(len(datasetStaffs)) + " entries")
print("import complete")
