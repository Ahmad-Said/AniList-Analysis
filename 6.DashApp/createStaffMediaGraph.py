import dash_cytoscape as cyto
import networkx as nx
import setting


def createStaffMediaGraph(targetMedias):
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

    # elements of the cytoscape graph
    elements = []

    # collect each staff at which media he participated so we can form parent group
    staffToMediaParent = {}
    staffToMediaEdges = {}
    for index, media in targetMedias.iterrows():
        staffList = mediaToStaffList[media.id]
        mediaNodeId = 'm' + str(media.id)
        for staffId in staffList:
            G.add_edge(mediaNodeId, staffId)
            # affecting staff nodes to first media participated in
            # if already affected to another media add edge from staff to media group
            if staffId not in staffToMediaParent:
                staffToMediaParent[staffId] = mediaNodeId
            else:
                # add additonal edge to media group
                if staffId not in staffToMediaEdges:
                    staffToMediaEdges[staffId] = [mediaNodeId]
                else:
                    staffToMediaEdges[staffId].append(mediaNodeId)

    # Remove outlier media where its staff are only connected to it
    if setting.removeMediaOutlierByDefault[0] and len(targetMedias) > 1:
        for index, media in targetMedias.iterrows():
            staffList = mediaToStaffList[media.id]
            mediaNodeId = 'm' + str(media.id)
            isOutlier = True
            for staffId in staffList:
                if G.degree[staffId] > 1:
                    isOutlier = False
            if isOutlier:
                print("Removing outlier media id " + mediaNodeId)
                G.remove_node(mediaNodeId)
                for staffId in staffList:
                    staffToMediaParent.pop(staffId, None)
                    staffToMediaEdges.pop(staffId, None)
                    G.remove_node(staffId)

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # clear staffs that have the least edges
    atLeastInXMedia = setting.staffAtLeastInXMedia[0]
    espaceNodes = setting.nodeGraphEspacement[0]

    for staffId in list(staffToMediaParent.keys()):
        if atLeastInXMedia <= 1:
            break
        # deduce one because every staff is already in parent media without edge
        if staffId not in staffToMediaEdges or len(staffToMediaEdges[staffId]) < atLeastInXMedia - 1:
            staffToMediaParent.pop(staffId, None)
            staffToMediaEdges.pop(staffId, None)
            G.remove_node(staffId)

    # creating parents nodes as medias
    for index, media in targetMedias.iterrows():
        # add m to media id to prevent conflict with staff id
        mediaNodeId = 'm' + str(media.id)
        # skip outlier medias that may be removed from G
        if not G.has_node(mediaNodeId):
            continue
        elements.append({
            'data': {'id': mediaNodeId, 'label': media.title_userPreferred},
            'position': {'x': pos[mediaNodeId][0] * len(G.nodes) * espaceNodes,
                         'y': pos[mediaNodeId][1] * len(G.nodes) * espaceNodes},
            'classes': 'triangle'
        })
        G.remove_node(mediaNodeId)

    #  creating nodes graphs
    for node in G.nodes():
        x, y = pos[node]
        elements.append({
            'data': {'id': str(node), 'label': str(node), 'parent': staffToMediaParent[node]},
            'position': {'x': x * len(G.nodes) * espaceNodes, 'y': y * len(G.nodes) * espaceNodes},
        })
        for mediaEdge in staffToMediaEdges[node] if node in staffToMediaEdges else []:
            elements.append({'data': {'source': str(node), 'target': mediaEdge}})

    # creating strong edges
    for edge in G.edges():
        weight = G.get_edge_data(edge[0], edge[1])['weight']
        # if weight > 1:
        #     elements.append({'data': {'source': str(edge[0]), 'target': str(edge[1]), 'weight': weight}})
    # return elements
    return cyto.Cytoscape(
        id='staffGraph',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '900px'},
        elements=elements,
        stylesheet=setting.stylesheetGraph
    )
