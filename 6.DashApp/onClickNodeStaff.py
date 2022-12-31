import dash_bootstrap_components as dbc
from dash import Input, Output, dash_table, callback
from dash import html

import setting
from prepareData import *


@callback(Output('selectedGraphNode', 'children'), Input('staffGraph', 'selectedNodeData'))
def onSelectedNodeData(selectedNodeData):
    if not selectedNodeData:
        return ''
    tempDf = pandas.DataFrame(selectedNodeData).filter(like='id')

    # collect list of medias selected
    selectedDataMediaIds = tempDf[tempDf.id.str.startswith('m')].applymap(lambda x: x[1:])
    selectedDataMediaIds = set(pandas.to_numeric(selectedDataMediaIds.id))
    selectedNodeMedias = datasetMedias[datasetMedias.index.isin(selectedDataMediaIds)]

    # collect list of staffs selected
    selectedDataStaffsIds = tempDf[~tempDf.id.str.startswith('m')]
    selectedDataStaffsIds = set(pandas.to_numeric(selectedDataStaffsIds.id))
    selectedNodeStaffs = datasetStaffs[datasetStaffs.index.isin(selectedDataStaffsIds)]

    # determine role of staff in media if only one staff is selected
    displayMediaWithRoles = setting.displayMediaColumns.copy()
    displayStaffWithRoles = setting.displayStaffColumns.copy()
    header = ''
    if len(selectedDataStaffsIds) == 1:
        displayMediaWithRoles.append('Role')
        staffId = next(iter(selectedDataStaffsIds))
        # display roles on all target media, otherwise filter by selection over medias
        if len(selectedNodeMedias) == 0:
            selectedNodeMedias = setting.targetMediasGl[0]
        roles = []
        particpatedIn = 0
        for index, media in selectedNodeMedias.iterrows():
            edges = media.staff['edges']
            found = False
            for edge in edges:
                if edge['node']['id'] == staffId:
                    found = True
                    roles.append(edge['role'])
                    particpatedIn += 1
                    break
            if not found:
                roles.append("Did not participate")
        selectedNodeMedias['Role'] = roles
        selectedNodeMedias.sort_values(by=['Role'], inplace=True)
        header = 'Staff particpated in ' + str(particpatedIn) + ' medias of total ' + str(len(selectedNodeMedias))

    elif len(selectedNodeMedias) == 1:
        # list of all characters in specific medias and their roles
        displayStaffWithRoles.append('Role')
        mediaId = next(iter(selectedDataMediaIds))
        # display roles on all target media, otherwise filter by selection over medias
        roles = []
        media = selectedNodeMedias.iloc[0]
        edges = media.staff['edges']
        for edge in edges:
            roles.append({'id': edge['node']['id'], 'Role': edge['role']})
        rolesDf = pandas.DataFrame(roles)
        rolesDf.index = rolesDf.id
        selectedNodeStaffs = datasetStaffs[datasetStaffs.id.isin(rolesDf.id)].join(rolesDf['Role'])
        header = 'This media have ' + str(len(edges)) + ' staffs'

    htmlElemnts = [
        dash_table.DataTable(selectedNodeStaffs[displayStaffWithRoles].astype(str).to_dict('records'),
                             cell_selectable=False,
                             id='selectedNodesStaffs') if len(selectedNodeStaffs) != 0 else '',
        html.Br(),
        dash_table.DataTable(selectedNodeMedias[displayMediaWithRoles].astype(str).to_dict('records'),
                             cell_selectable=False, editable=True,
                             id='selectedNodesMedias') if len(selectedNodeMedias) != 0 else '',
    ]

    if (len(selectedNodeMedias) == 1):
        htmlElemnts.reverse()

    htmlElemnts.insert(0, dbc.Label(header))

    return dbc.Container(htmlElemnts)
