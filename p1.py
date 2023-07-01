import socket
import time
import json
from tabulate import tabulate
import psycopg2

host = ''
port = 5555
con = socket.socket()

con.bind(('localhost', port))
con.listen()

i = 0
addresses = []

def treeTable(tree):
    table = []
    typesList = []

    # 1: Camera
    # 2: WiFi

    psql = psycopg2.connect(user='postgres', password='samrith123', dbname='sensorData')

    cursor = psql.cursor()


    cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='cameradata');")
    cameraExists = cursor.fetchone()[0]

    if cameraExists == False:
        cursor.execute("CREATE TABLE cameraData (Time varchar, String varchar);")

    cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='wifidata');")
    wifiExists = cursor.fetchone()[0]

    if wifiExists == False:
        cursor.execute("CREATE TABLE wifidata (Time varchar, Uif varchar, Mac varchar);")
    table = []

    # 1: Camera
    # 2: WiFi

    for key in tree.keys():
        match tree[key]['sensorType']:
            case 1:
                for branch in range(len(tree[key]['data'])):
                        for node in tree[key]['data'][branch]['data']:
                            data = node['data']
                            if('time' in data and 'string' in data):
                                table.append([data['time'], data['string']])
                for value in table:
                    cursor.execute("INSERT INTO cameradata (Time, String) VALUES (%s, %s);", (value[0], value[1]))
                table.clear()
            case 2:
                for branch in range(len(tree[key]['data'])):
                        for node in tree[key]['data'][branch]['data']:
                            data = node['data']
                            if('time' in data and 'uif' in data and 'mac' in data):
                                table.append([data['time'], data['uif'], data['mac']])
                for value in table:
                    cursor.execute("INSERT INTO wifidata (Time, Uif, Mac) VALUES (%s, %s, %s);", (value[0], value[1], value[2]))
                table.clear()


    psql.commit()
    cursor.close()
    psql.close()



while True:
    connection, address = con.accept()
    addresses.append(address)
    if address != addresses[i-1]:
        print(f"New Connection From {address}")
    elif len(addresses) == 1:
        print(f"New Connection From {address}")
    data = connection.recv(4096)
    tree = json.loads(data.decode('utf-8'))
    treeTable(tree)
    
    i += 1
    connection.close()
    

    
    
    
    
        
    