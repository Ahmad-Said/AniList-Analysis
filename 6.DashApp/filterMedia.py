import numbers
import time

import dash_bootstrap_components as dbc
from dash import Input, Output, dash_table, ctx
from dash.exceptions import PreventUpdate

import setting
from app import app
from createStaffMediaGraph import *
from createStaffGraph import *
from prepareData import *

triggerTime = time.time()
triggerCounts = 0

clearElements = False


@app.callback(
    [
        Output('mediaFounds', 'children'),
        Output('staffGraphContainer', 'children')
    ],
    [
        Input('mediaName', 'value'),
        Input('showMediaNodes', 'value'),
        Input('removeMediaOutlier', 'value'),
        Input('staffAtLeastInXMedia', 'value'),
        Input('nodeGraphEspacement', 'value'),
    ]
)
def searchMedia(mediaName, showMediaNodes, removeMediaOutlier, staffAtLeastInXMedia, nodeGraphEspacement):
    setting.removeMediaOutlierByDefault[0] = removeMediaOutlier
    try:
        setting.staffAtLeastInXMedia[0] = int(staffAtLeastInXMedia)
    except:
        print(str(staffAtLeastInXMedia) + " staffAtLeastInXMedia value is not integer")
    try:
            setting.nodeGraphEspacement[0] = int(nodeGraphEspacement)
    except:
        print(str(nodeGraphEspacement) + " nodeGraphEspacement value is not integer")

    global triggerTime
    global triggerCounts
    triggerCounts += 1
    lastCallFromXSeconds = time.time() - triggerTime
    currentTrigger = triggerCounts
    triggerTime = time.time()

    if setting.preventConsecutiveUpdate[0] and lastCallFromXSeconds < setting.preventConsecutiveUpdate[1]:
        # wait for 0.5 second so other concurrent calls can finish their tasks
        time.sleep(0.5)
        if currentTrigger < triggerCounts:
            print('Horray prevented one update!')
            # prevent consecutive update and only take last one
            raise PreventUpdate
    # if ctx.triggered_id == 'showMediaNodes' and not showMediaNodes:
    #     return '', ''
    if not mediaName or len(mediaName) == 0:
        return '', ''
    # Get only medias related to specific media in parameter
    # search media titles ignoring case and ignoring none value
    targetMedia = datasetMedias[mediaTitles.title_userPreferred.str.contains(mediaName, na=False, case=False)]

    if len(targetMedia) == 0:
        return ['no media with such name was found', ''], ''
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
        dash_table.DataTable(targetMedias[setting.displayMediaColumns].astype(str).to_dict('records'),
                             cell_selectable=False,
                             editable=True,
                             id='targetMedias', page_size=5),
    ])
    if len(targetMedias) != 0:
        # return [searchResult, createStaffGraph(targetMedias)], ''
        return [searchResult,
                createStaffMediaGraph(targetMedias) if showMediaNodes else createStaffGraph(targetMedias)], ''
    else:
        return ['no result found', ''], ''
