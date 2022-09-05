import json


def searchByName(name):
    if name == '':
        return json.dumps({'code': 2001, 'message': '请输入设备名称'})
    file = open("D:\\graduation-project\\demo\\backend\\data\\graph4.json", "r")
    data = json.load(file)
    nodes = list(data['nodes'])
    links = list(data['links'])
    # id2node是节点id到节点对象的映射
    id2node = {}
    # id2Set是节点id到关联节点id集合的映射
    id2Set = {}
    # searchResult是搜索得到的节点.
    searchResult = None
    for node in nodes:
        if name == node['name'] and node['classof'] == 1:
            searchResult = node
        id2node[node['id']] = node
    if searchResult is not None:
        code = 2000
        newNodes = [searchResult, ]
        newLinks = []
        newNodesSet = set(searchResult['id'])
        for link in links:
            if link['source'] not in id2Set:
                id2Set[link['source']] = set()
            id2Set[link['source']].add(link['target'])
            if searchResult['id'] == link['source'] and link['target'] not in newNodesSet and '主变' not in id2node[link['target']]['name']:
                newNodes.append(id2node[link['target']])
                newLinks.append(link)
                newNodesSet.add(link['target'])
            elif searchResult['id'] == link['target'] and link['source'] not in newNodesSet:
                newNodes.append(id2node[link['source']])
                newLinks.append(link)
                newNodesSet.add(link['source'])
        imgsrc = ''
        tableData = []
        for node in newNodes:
            if node['classof'] == 3:
                imgsrc = node['imgsrc']
            if node['classof'] == 2:
                harm = '未知危害'
                level = '未知'
                measure = '暂无对应解决措施'
                if node['id'] in id2Set:
                    for id_ in id2Set[node['id']]:
                        if id2node[id_]['classof'] == 4:
                            harm = id2node[id_]['name']
                        elif id2node[id_]['classof'] == 6:
                            if measure == '暂无对应解决措施':
                                measure = id2node[id_]['content']
                            else:
                                measure = measure + '; '+ id2node[id_]['content']
                        elif id2node[id_]['classof'] == 9 and id2node[id_]['name'] != 'None':
                            level = id2node[id_]['name']
                tableData.append({
                    '缺陷': node['name'],
                    '危害': harm,
                    '等级': level,
                    '措施': measure
                })

        result = json.dumps({'code': code, 'node': searchResult, 'imgsrc': imgsrc, 'tableData': tableData, 'graph': {'nodes': newNodes, 'links': newLinks}})
    else:
        code = 2002
        message = '未查询到相关设备'
        result = json.dumps({'code': code, 'message': message})
    return result

