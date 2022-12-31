import matplotlib.pyplot as plt
import warnings
import plotly.graph_objects as go

import networkx as nx
import pandas as pd, pandas
import ast
from pandas import json_normalize
import re
import seaborn as sns
import numpy

# https://plotly.com/python/network-graphs/
# read dataset from json file
# https://github.com/catboost/catboost/issues/2179
warnings.simplefilter(action='ignore', category=FutureWarning)
datasetMedias = pandas.read_json("../data/split/medias/medias1.json")
print("reading medias done")
datasetStaffs = pandas.read_json("../data/split/staffs/staffs1.json")
print("reading staffs done")


def list_of_dicts(ld):
    """
    Create a mapping of the tuples formed after
    converting json strings of list to a python list
    see https://stackoverflow.com/questions/39899005/how-to-flatten-a-pandas-dataframe-with-some-columns-as-json
    """
    return dict([(list(d.values())[1], list(d.values())[0]) for d in ast.literal_eval(ld)])


titles = json_normalize(datasetMedias['title'].tolist()).add_prefix('title_')
datasetMedias = datasetMedias.join(titles)

datasetMedias.index = datasetMedias.id
datasetStaffs.index = datasetStaffs.id
titles.index = datasetMedias.index

# Get only medias related to specific animation
nameOfAnimation = "Cowboy"
# search media titles ignoring case and ignoring none value
targetMedia = datasetMedias[titles.title_english.str.contains(nameOfAnimation, na=False, case=False)]

if len(targetMedia) == 0:
    print("no media with such name was found")
    exit()

# get the first media found
firstMediaFound = targetMedia.loc[targetMedia.index[0]]
#  use relations attributes to collect others related medias in series
# relations -> nodes -> [{"id":value}]
# extract relations nodes id to list
targetRelatedMediasIds = pandas.DataFrame(firstMediaFound.relations['nodes']).id.to_list()
targetRelatedMediasIds.append(firstMediaFound.id)
targetMedias = datasetMedias[datasetMedias.id.isin(targetRelatedMediasIds)]

if len(targetRelatedMediasIds) != len(targetMedias):
    print("Media node ids " + str(list(set(targetRelatedMediasIds) - set(targetMedias.id)))
          + " was not found in dataset")

# create graph
G = nx.Graph()
for index, media in targetMedias.iterrows():
    nodes = media.staff['nodes']
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            G.add_edge(nodes[i]['id'], nodes[j]['id'])

pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility


edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))


node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text


fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Network graph made with Python',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()




print("setup complete")
