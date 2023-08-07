import socket
import time
import json

tree = {}
con = socket.socket()
port = 5555
con.connect(('localhost', port))

def insertNode(data, parentId, typeId, Id, sensorId = -1):

    if(sensorId != -1):
        node = {"data": data, "type": typeId, "Id": Id, "sensorType": sensorId}
    else:
        node = {"data": data, "type": typeId, "Id": Id}
    nodesList = []

    nodesList.append(node)

    if typeId == 1: #this node is a root.
        tree[Id] = node
    else:
        for branch in tree:
            Id = tree[branch]['Id']
            data = tree[branch]['data']
            if(parentId == Id):
                for branchNode in data:
                    nodesList.append(branchNode)
                tree[branch]['data'] = nodesList
                break
            else:
                for leaf in range(len(data)):
                    if(data[leaf]['Id'] == parentId):
                        for leafNode in data[leaf]['data']:
                            nodesList.append(leafNode)
                        data[leaf]['data'] = nodesList
            
                
                    
 

insertNode({}, 0, 1, 1, 1)
insertNode({}, 0, 1, 2, 2)

insertNode({}, 1, 2, 3)
insertNode({}, 2, 2, 4)

insertNode({"time": "14:00", "string": 'img1'}, 3, 3, 5)
insertNode({"time": "14:03", "string": 'img2'}, 3, 3, 6)

insertNode({"time": "14:03", "uif": '??', 'mac': ['15-79-A0-C3-00-55', '45-89-4F-88-A9-42', '9E-D2-71-27-FC-21']}, 4, 3, 7)
insertNode({"time": "14:03", "uif": '??', 'mac': ['B3-9C-C9-2D-B2-BB', '8E-EA-F7-98-91-8E', 'F3-8B-55-B4-2E-5E']}, 4, 3, 8)


tree = json.dumps(tree)

con.sendall(bytes(tree, encoding='utf-8'))

con.close()
    