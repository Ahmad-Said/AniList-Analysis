import dash_cytoscape as cyto
import networkx as nx


def createStaffGraph(targetMedias):
    # create graph
    G = nx.Graph()

    # collecting staffs participating in medias and clearing duplicate values
    mediaToStaffList = {}
    for index, media in targetMedias.iterrows():
        edges = media.staff['edges']
        staffIds = set()
        for edge in edges:
            staffIds.add(edge['node']['id'])
        mediaToStaffList[media.id] = list(staffIds)
    for index, media in targetMedias.iterrows():
        staffList = mediaToStaffList[media.id]
        for i in range(len(staffList)):
            for j in range(i + 1, len(staffList)):
                a = staffList[i]
                b = staffList[j]
                if a == b:
                    continue
                if not G.has_edge(a, b):
                    G.add_edge(a, b, weight=1)
                else:
                    G.add_edge(a, b, weight=G.get_edge_data(a, b)['weight'] + 1)

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    elements = []

    #  creating nodes graphs
    for node in G.nodes():
        x, y = pos[node]
        elements.append({'data': {'id': str(node), 'label': str(node)},
                         'position': {'x': x * len(G.nodes) * 30, 'y': y * len(G.nodes) * 30}})

    # creating strong edges
    for edge in G.edges():
        elements.append({'data': {'source': str(edge[0]), 'target': str(edge[1])}})

    return cyto.Cytoscape(
        id='staffGraph',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '900px'},
        elements=elements,
    )
