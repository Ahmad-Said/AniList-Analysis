################################################################################
###
### IMPORTS
###
################################################################################
from dash import Dash, Input, Output, dash_table, State, callback
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import setting

################################################################################
###
### SETUP
###
################################################################################
# create Dash instance app before importing callback in separated file
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# read dataset
from importData import *
from prepareData import *

################################################################################
###
### LAYOUT
###
################################################################################
app.layout = dbc.Container([
    dbc.Checkbox(id='showMediaNodes', label='Showing Media nodes', value=setting.showMediaNodeByDefault[0]),
    dbc.Checkbox(id='removeMediaOutlier', label='Remove Media outlier', value=setting.removeMediaOutlierByDefault[0]),
    dbc.Label('Only Staff at least in X Media : '),
    dbc.Input(id='staffAtLeastInXMedia', value=setting.staffAtLeastInXMedia[0]),
    dbc.Label('Node graph espacement: '),
    dbc.Input(id='nodeGraphEspacement', value=setting.nodeGraphEspacement[0]),
    dbc.Label('Media Name: '),
    dbc.Input(id='mediaName'),
    dbc.Alert(id='mediaFounds'),
    dbc.Container(id='showMediasNodesOutput'),
    dbc.Container([
        cyto.Cytoscape(id='staffGraph',
                       layout={'name': 'preset'},
                       style={'width': '100%', 'height': '900px'},
                       elements=[])
    ], id='staffGraphContainer'),
    dbc.Alert(id='selectedGraphNode'),
])



################################################################################
###
### CALLBACKS
###
################################################################################
from filterMedia import *
from onClickNodeStaff import *


if __name__ == "__main__":
    app.run_server(debug=True)
