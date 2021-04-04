# X001_Lock cp932
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, request, redirect, g
import os
import csv
import json
import sqlite3
import pandas as pd
import logging

format_str = '%(asctime)s - %(process)d - %(thread)d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format_str, level=logging.INFO)
logger = logging.getLogger(__name__)

format_date='%Y-%m-%d'

app = Flask(__name__)

def cn_open():
    cn = sqlite3.connect('./DB603LCK.db')
    cn.isolation_level = None
    cn.row_factory = sqlite3.Row
    return cn

#定数
cX001ID= 0
c日付= 1
cLayer= 2
cTableCode= 3
cRecordID= 4
cPCID= 5
cUserName= 6
cKK= 7
cSV= 8

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS X001_Lock '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS X001_Lock ('
    wsql+='X001ID TEXT  DEFAULT NULL PRIMARY KEY,'
    wsql+='日付 TEXT  DEFAULT NULL,'
    wsql+='Layer INTEGER  DEFAULT 0,'
    wsql+='TableCode TEXT  DEFAULT NULL,'
    wsql+='RecordID TEXT  DEFAULT NULL,'
    wsql+='PCID INTEGER  DEFAULT 0,'
    wsql+='UserName TEXT  DEFAULT NULL,'
    wsql+='KK INTEGER  DEFAULT 0,'
    wsql+='SV INTEGER  DEFAULT 0'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='X001ID, '
    wsql+='日付, '
    wsql+='Layer, '
    wsql+='TableCode, '
    wsql+='RecordID, '
    wsql+='PCID, '
    wsql+='UserName, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM X001_Lock '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO X001_Lock VALUES ('
    wsql+=':X001ID, '
    wsql+=':日付, '
    wsql+=':Layer, '
    wsql+=':TableCode, '
    wsql+=':RecordID, '
    wsql+=':PCID, '
    wsql+=':UserName, '
    wsql+=':KK, '
    wsql+=':SV '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE X001_Lock SET '
    wsql+='日付=:日付, '
    wsql+='Layer=:Layer, '
    wsql+='TableCode=:TableCode, '
    wsql+='RecordID=:RecordID, '
    wsql+='PCID=:PCID, '
    wsql+='UserName=:UserName, '
    wsql+='KK=:KK, '
    wsql+='SV=:SV '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM X001_Lock '
    return wsql

def get_primarykerfilter(ID):
    wID = '"' + ID + '"'
    wfilter=' WHERE X001ID = ' + wID +' '
    return wfilter

def get_X001(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/X001_index', methods=['GET'])
def get_X001_index():
    cn = cn_open()
    wsql = 'SELECT * FROM X001_Lock '
    wsql+= 'ORDER BY  X001ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X001_index.html',rows = rows )
    cn.close()

@app.route('/X001_insert', methods=['GET'])
def get_X001_insert():
    return render_template('X001_insert.html')

@app.route('/X001_insert', methods=['POST'])
def post_X001_insert():
    wsql = get_insert_sql()
    wX001ID = request.form.get('X001ID')    #0
    w日付 = request.form.get('日付')    #1
    wLayer = request.form.get('Layer')    #2
    wTableCode = request.form.get('TableCode')    #3
    wRecordID = request.form.get('RecordID')    #4
    wPCID = request.form.get('PCID')    #5
    wUserName = request.form.get('UserName')    #6
    wKK = request.form.get('KK')    #7
    wSV = request.form.get('SV')    #8
    cn = cn_open()
    row = (
        wX001ID,
        w日付,
        wLayer,
        wTableCode,
        wRecordID,
        wPCID,
        wUserName,
        wKK,
        wSV
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM X001_Lock '
    wsql+= 'ORDER BY  X001ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X001_index.html',rows = rows )
    cn.close()

@app.route('/X001_detail/<ID>', methods=['GET'])
def get_X001_detail(ID):
    data = get_X001(ID)
    return render_template('X001_detail.html', X001=data)

@app.route('/X001_update/<ID>', methods=['GET'])
def get_X001_update(ID):
    data = get_X001(ID)
    return render_template('X001_update.html', X001=data)

@app.route('/X001_update/<ID>', methods=['POST'])
def post_X001_update(ID):
    data = get_X001(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w日付 = request.form.get('日付')    #1
    wLayer = request.form.get('Layer')    #2
    wTableCode = request.form.get('TableCode')    #3
    wRecordID = request.form.get('RecordID')    #4
    wPCID = request.form.get('PCID')    #5
    wUserName = request.form.get('UserName')    #6
    wKK = request.form.get('KK')    #7
    wSV = request.form.get('SV')    #8
    cn = cn_open()
    row = {
        '日付':w日付,
        'Layer':wLayer,
        'TableCode':wTableCode,
        'RecordID':wRecordID,
        'PCID':wPCID,
        'UserName':wUserName,
        'KK':wKK,
        'SV':wSV
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_X001(ID)
    return render_template('X001_detail.html', X001=data)


@app.route('/X001_delete/<ID>', methods=['GET'])
def get_X001_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM X001_Lock '
    wsql+= 'ORDER BY  X001ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X001_index.html',rows = rows )
    cn.close()

@app.route('/X001_importcsv',methods=['GET'])
def get_X001_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('X001.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/X001_exportjson',methods=['GET'])
def get_X001_exportjson():
    wsql = X001_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    X001s=[
    dict(
        X001ID = row[0],
        日付 = row[1],
        Layer = row[2],
        TableCode = row[3],
        RecordID = row[4],
        PCID = row[5],
        UserName = row[6],
        KK = row[7],
        SV = row[8]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if X001s is not None:
        return json.dump(X001s,ensure_ascii=False,indent=4)

@app.route('/X001_initialize',methods=['GET'])
def get_X001_initialize():

    cn = cn_open()

    # Drop
    wsql = get_drop_sql()
    cn.execute(wsql)

    #Create
    wsql = get_create_sql()
    cn.execute(wsql)

    #Insert
    wsql = get_insert_sql()
    for row in rows:
        cn.execute(wsql, row)

    #Select to ,jsonformat
    wsql = get_select_sql()
    rows =cn.execute(wsql)
    X001s=[
        dict(
            X001ID = row[0],
            日付 = row[1],
            Layer = row[2],
            TableCode = row[3],
            RecordID = row[4],
            PCID = row[5],
            UserName = row[6],
            KK = row[7],
            SV = row[8]
            )
        for row in rows.fetchall()
        ]
    if X001s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'X001.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(X001s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_X001_initialize()

"""

@app.route('/X001_index', methods=['GET'])
def get_X001_index():
    return X001.get_X001_index()

@app.route('/X001_insert', methods=['GET'])
def get_X001_insert():
    return X001.get_X001_insert()

@app.route('/X001_insert', methods=['POST'])
def post_X001_insert():
    return X001.post_X001_insert()

@app.route('/X001_importcsv', methods=['GET'])
def get_X001_jimportcsv():
    X001.get_X001_importcsv()
    return X001.get_X001_index()

@app.route('/X001_json', methods=['GET'])
def get_X001_json():
    return X001.get_X001_json()

@app.route('/X001_detail/<ID>', methods=['GET'])
def get_X001_detail(ID):
    return X001.get_X001_detail(ID)

@app.route('/X001_update/<ID>', methods=['GET'])
def get_X001_update(ID):
    return X001.get_X001_update(ID)

@app.route('/X001_update/<ID>', methods=['POST'])
def post_X001_update(ID):
    return X001.post_X001_update(ID)

@app.route('/X001_delete/<ID>', methods=['GET'])
def get_X001_delete(ID):
    return X001.get_X001_index(ID)

#createtableX001.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = './DB603LCK.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  X001_Lock)

# Drop
wsql = get_drop_sql()
cn.execute(wsql)

#Create
wsql = get_create_sql()
cn.execute(wsql)

#data
rows = (
    {'ID': 1, 'NAME': '受注入力', 'HREF':'/M011_index','CATEGORY': 1, 'ENABLED': 1, 'SECURITYLEVEL': 0, 'MEMO': '受注書、発注書'},
    {'ID': 2, 'NAME': '売上入力', 'HREF':'/M111_index','CATEGORY': 1, 'ENABLED': 1, 'SECURITYLEVEL': 0, 'MEMO': '納品書、納品請求書'},
    )

#Insert
wsql = get_insert_sql()
for row in rows:
    cn.execute(wsql, row)

#Select to ,jsonformat
wsql = get_select_sql()
rows = cn.execute(wsql)
X001s=[
    dict(
        X001ID = row[0],
        日付 = row[1],
        Layer = row[2],
        TableCode = row[3],
        RecordID = row[4],
        PCID = row[5],
        UserName = row[6],
        KK = row[7],
        SV = row[8]
        )
    for row in rows.fetchall()
    ]
if X001s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'X001.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(X001s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
