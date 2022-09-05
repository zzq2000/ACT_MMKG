import json


def getGraph(graph_id):
    file_path = 'D:\\graduation-project\\demo\\backend\\data\\'
    if graph_id == '0':
        file_path += 'graph1.json'
    elif graph_id == '1':
        file_path += 'graph2.json'
    elif graph_id == '2':
        file_path += 'graph3.json'
    elif graph_id == '3':
        file_path += 'graph4.json'
    else:
        return json.dumps({'code': 1001, 'message': '图谱编号不存在'})
    file = open(file_path, "r")
    data = json.load(file)
    nodes = list(data['nodes'])
    links = list(data['links'])
    newNodes = []
    newLinks = []
    newIdSet = set()
    idSet = set()
    for link in links:
        idSet.add(link['source'])
        idSet.add(link['target'])
    for i, node in enumerate(nodes):
        if node['id'] in idSet and i < 30:
            newNodes.append(node)
            newIdSet.add(node['id'])
    for link in links:
        if link['source'] in newIdSet and link['target'] in newIdSet:
            newLinks.append(link)
    nodeClassSum = {}
    name = ['设备', '缺陷', '图片', '危害', '成因', '措施', '设备型号', '状态量', '缺陷分类', '分类依据', '判断依据']
    for node in nodes:
        nodeName = name[int(node['classof']) - 1]
        if nodeName not in nodeClassSum:
            nodeClassSum[nodeName] = 0
        nodeClassSum[nodeName] += 1
    nodeClassSumList = list(nodeClassSum.items())
    nodeClassSumListRanked = sorted(((value, key) for key, value in nodeClassSumList), reverse=True)
    xData = [key for (value, key) in nodeClassSumListRanked]
    yData = [value for (value, key) in nodeClassSumListRanked]
    linkClassSum = {}
    for link in links:
        if link['name'] not in linkClassSum:
            linkClassSum[link['name']] = 0
        linkClassSum[link['name']] += 1
    linkClassSumList = list(linkClassSum.items())
    linkClassSumListRanked = sorted(((value, key) for key, value in linkClassSumList), reverse=True)
    pieChartData = [{'value': value, 'name': key} for (value, key) in linkClassSumListRanked]
    result = json.dumps({'code': 1000, 'nodes': newNodes, 'links': newLinks, 'barChartData': {'xData': xData, 'yData': yData},
                        'pieChartData': pieChartData})
    return result


