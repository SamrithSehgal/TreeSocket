import socket
import time
import json
from tabulate import tabulate
import psycopg2
from collections import defaultdict

host = ''
port = 5555
con = socket.socket()

con.bind(('localhost', port))
con.listen()

i = 0
addresses = []

psql = psycopg2.connect(user='postgres', password='samrith123', dbname='sensorData')
cursor = psql.cursor()

table = []




def exists(tableName, parameters):
    command = f'CREATE TABLE {tableName} ('
    cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s);", (tableName,))
    tableExists = cursor.fetchone()[0]
    
    for param in parameters.keys():
        command = command + f'{param} {parameters[param]}, '
    command = command[:len(command) - 2] + ')'

    if tableExists == False:
        cursor.execute(command)
    psql.commit()

def insertData(tableName, key):
    tableData = []
    params = []
    tableInfo = {}

    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name=%s;", (tableName,))
    tableParams = cursor.fetchall()

    for param in tableParams:
        params.append(param[0])
        
    allParams = ', '.join(params)
    command = f'INSERT INTO {tableName}({allParams}) VALUES ('
    for value in range(len(params)):
        command = command + '%s, '
    command = command[:len(command) - 2] + ')'
    
    
    tableInfo[tableName] = params
    
    for branch in range(len(tree[key]['data'])):
        for node in tree[key]['data'][branch]['data']:
            data = node['data']
            for info in tableInfo[tableName]:
                if(info not in data):
                    return 'Error'
                else:
                    tableData.append(data[info])
            table.append(tableData)
            tableData = []

    for value in table:
        value = tuple(value)
        cursor.execute(command, value)
    table.clear()

exists('cameradata', {'Time': 'varchar', 'String': 'varchar'})
exists('wifidata', {'Time': 'varchar', 'Uif': 'varchar', 'Mac': 'varchar'})

cursor.execute("SELECT table_name, column_name FROM information_schema.columns WHERE table_name IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public');")
cols = cursor.fetchall()

def treeTable(tree):
    for key in tree.keys():
        match tree[key]['sensorType']:
            case 1:
                insertData('cameradata', key)
            case 2:
                insertData('wifidata', key)


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
    

    
    
    
    
        
    