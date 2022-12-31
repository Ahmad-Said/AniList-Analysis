import dash_bootstrap_components as dbc
from dash import Input, Output, dash_table, State

import setting
from app import app
from createStaffMediaGraph import *
from prepareData import *


@app.callback(
    [
        Output('mediaFounds', 'children'),
        Output('staffGraph', 'zoom'),
        Output('staffGraph', 'layout'),
        Output('staffGraph', 'elements')
    ],
    [
        Input('mediaName', 'value')
    ],
    [
        State('staffGraph', 'layout'),
        State('staffGraph', 'elements')
    ]
)
def searchMedia(mediaName, layout, elements):
    if not mediaName or len(mediaName) == 0:
        return ['', 1, layout, elements]
    # Get only medias related to specific media in parameter
    # search media titles ignoring case and ignoring none value
    targetMedia = datasetMedias[mediaTitles.title_userPreferred.str.contains(mediaName, na=False, case=False)]

    if len(targetMedia) == 0:
        return ['no media with such name was found', 1, layout, elements]

    # get the first media found
    firstMediaFound = targetMedia.loc[targetMedia.index[0]]
    targetRelatedMediasIds = [firstMediaFound.id]
    #  use relations attributes to collect others related medias in series
    # relations -> nodes -> [{"id":value}]
    # extract relations nodes id to list
    if len(firstMediaFound.relations['nodes']) > 0:
        targetRelatedMediasIds += pandas.DataFrame(firstMediaFound.relations['nodes']).id.to_list()
    targetMedias = datasetMedias[datasetMedias.id.isin(targetRelatedMediasIds)]
    # remove medias that have empty staff list
    targetMedias = targetMedias[targetMedias.staff.map(lambda x: len(x['edges']) > 0)]
    setting.targetMediasGl[0] = targetMedias
    if len(targetRelatedMediasIds) != len(targetMedias):
        print("Media node ids " + str(list(set(targetRelatedMediasIds) - set(targetMedias.id)))
              + " was not found in dataset")
    searchResult = dbc.Container([
        dbc.ListGroup([
            dbc.ListGroupItem("Media found: " + firstMediaFound.title_userPreferred, color="primary"),
            dbc.ListGroupItem("Related medias count: " + str(len(targetMedias)), color="info"),
        ]),
        dash_table.DataTable(data=targetMedias[setting.displayMediaColumns].astype(str).to_dict('records'),
                             cell_selectable=False,
                             editable=True,
                             id='targetMedias', page_size=5),
    ])

    if len(targetMedias) != 0:
        return [searchResult, 1, layout, createStaffMediaGraph(targetMedias)]
    else:
        return ['no result found', 1, layout, elements]
